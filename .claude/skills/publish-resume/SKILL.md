---
name: publish-resume
description: |
  Publish the current resume to germankuber.com: copy `Resumes/Human/Germán Küber.pdf`
  into the personal-site repo AND mirror any content change into the site's rendered
  resume (`lib/data.ts` + `app/resume/page.tsx`), then commit and push — Vercel
  auto-deploys. The user invokes `/publish-resume`. Use this skill whenever the user
  wants the latest resume live on the website, asks to "publish the resume",
  "update the resume on the site", "sync the PDF to germankuber.com", or similar.
---

# Publish Resume Skill

You are the deploy step that takes the regenerated branded resume from
`Resumes/Human/` and puts it behind the "Download PDF" button on germankuber.com.
The user runs `/publish-resume` after they have already updated `Human/` (typically
via `/update-resume` Step 6.5–6.7) and now want it live.

This skill is the **only** sanctioned way to publish that PDF. Never copy by hand;
the two repos drift otherwise.

## Preconditions

Before doing anything, verify all of these. Stop and ask the user if any fail:

1. **The Human PDF exists** at `Resumes/Human/Germán Küber.pdf` (absolute path
   resolves to the current repo). If it does not exist, the user has not run
   `/update-resume` yet (Step 6.6 regenerates it) — tell them.
2. **The personal-site repo exists** at `../PersonalSite/personal-site/` relative
   to this repo — it is a *sibling of `Resumes/`* inside `Personal/`. The absolute
   path is
   `/Users/GermanKuber/Documents/Repositories/Personal/PersonalSite/personal-site`.
   If it is missing, clone it rather than asking the user to hunt for it:

   ```bash
   git clone https://github.com/germankuber/personal-site.git \
     ~/Documents/Repositories/Personal/PersonalSite/personal-site
   ```

   This is the personal `germankuber` account, not `nera-agro` — the default SSH
   identity works, no host alias needed.
3. **The personal-site repo is on `main` and clean** (or only has unrelated
   uncommitted changes the user is OK with). Run `git -C <personal-site> status`.
   If it is on a feature branch or has unstaged changes the user did not mention,
   stop and ask.
4. **`Resumes/Human/Germán Küber.pdf` is newer** than
   `personal-site/public/Germán Küber.pdf`. If the destination is newer, the user
   may be about to overwrite something they don't intend to — stop and confirm
   before continuing. Use `stat -f "%m  %N"` on both files to compare.

## Step 1 — Diff the PDFs

Compare the two PDFs by size and modification time:

```bash
stat -f "%Sm  %z  %N" -t "%Y-%m-%d %H:%M" \
  "Resumes/Human/Germán Küber.pdf" \
  "Personal/PersonalSite/personal-site/public/Germán Küber.pdf"
```

Report both lines to the user. If the sizes are identical and the timestamps are
within a minute, the publish is likely a no-op (the user already published this
exact PDF). Ask them whether to continue anyway (sometimes useful, e.g. to trigger
a Vercel rebuild after an unrelated issue).

## Step 2 — Copy the PDF

```bash
cp "Resumes/Human/Germán Küber.pdf" \
   "Personal/PersonalSite/personal-site/public/Germán Küber.pdf"
```

After the copy, run the `stat` comparison again and confirm the destination now
matches the source (same byte count).

## Step 2.5 — Sync the rendered resume on the site (REQUIRED)

The PDF is only the *download*. germankuber.com also renders the resume as HTML,
and that content lives in the site code — **not** in the PDF. If you publish the
PDF alone, the page and the download contradict each other.

The rendered resume is duplicated in two places, both of which must be updated:

- `lib/data.ts` — `personalInfo.bio` and the `experiences` array (shared data,
  used by the home page).
- `app/resume/page.tsx` — the summary paragraph and the `<ExperienceItem />`
  list (the `/resume` page has its own hardcoded copy).

For any factual change made in `Resumes/Human/resume.html` (a new role, a changed
title, corrected dates, a new metric), mirror it into BOTH files. Newest role
goes first in `experiences` and first in the `<ExperienceItem />` list.

`components/sections/Companies.tsx` is a logo grid — only add an entry there when
the employer is public and has a logo. Skip it for NDA / unnamed clients.

Then verify it compiles before committing:

```bash
cd <personal-site> && pnpm run build
```

`npm` is disabled on this machine — always use `pnpm`. Confirm the build succeeds
and `/resume` still prerenders.

## Step 3 — Commit and push in personal-site

The personal-site repo is independent. Operate inside it with `git -C` or by
changing directory.

1. `git -C <personal-site> add "public/Germán Küber.pdf"` — plus `lib/data.ts` and
   `app/resume/page.tsx` if Step 2.5 changed them.
2. `git -C <personal-site> status` — confirm only those files are staged. If any
   other unexpected file is staged, stop and ask the user.
3. `git -C <personal-site> commit -m "<message>"` — use this exact body shape
   (no Co-Authored-By tag; attribution is disabled globally per the user's
   `~/.claude/settings.json`):

   ```
   chore: refresh downloadable resume PDF

   Sync the branded resume PDF from Resumes/Human/ to the personal-site
   public/ folder so the "Download PDF" button on germankuber.com delivers
   the latest version.
   ```

4. `git -C <personal-site> push origin main`.

## Step 4 — Verify Vercel picked up the push

The personal-site project on Vercel auto-deploys from `main`. Use the Vercel MCP
to confirm a new deployment kicked off after the push.

1. The project is `personal-site` under the `kliver` scope. The known IDs:
   - `teamId`: `team_4ic1hmQWdiIfP1izezjVRFLx`
   - `projectId`: `prj_FV8iFctJJHRhJzr6qWxfwzUcUnGT`

   If these ever stop working, fall back to `mcp__vercel__list_teams` →
   `mcp__vercel__list_projects` to rediscover them.

2. Call `mcp__vercel__get_project` with those IDs. Confirm `latestDeployment` has
   a `createdAt` timestamp that is *after* your `git push`, and that
   `readyState` is either `BUILDING` or `READY`.

3. If `BUILDING`, that's fine — report the deploy ID and tell the user the build
   typically completes in 60–120 seconds. If they want, wait and re-check.
4. If `READY` already, the build finished — report success.
5. If the timestamp is older than the push, Vercel has not received the webhook
   yet; wait 10–20 seconds and re-call. If still stale after a minute, tell the
   user and stop — something is wrong with the GitHub → Vercel webhook and you
   should not retry blindly.

**If the Vercel MCP is not connected** (it often is not), verify against the live
site instead. Poll until the deployed content actually changes — do not just wait
a fixed time and declare success:

```bash
# PDF: poll until the served content-length matches the new file's byte count
until [ "$(curl -sI 'https://germankuber.com/Germ%C3%A1n%20K%C3%BCber.pdf' \
  | rg -i '^content-length:' | tr -d '\r' | awk '{print $2}')" = "<NEW_BYTES>" ]; do
  sleep 15
done

# Rendered resume: poll until the new content is present in the HTML
until curl -s 'https://germankuber.com/resume' | rg -q '<NEW_ROLE_TITLE>'; do
  sleep 15
done
```

Run these with `run_in_background: true` rather than blocking the turn.

## Step 5 — Report

Tell the user:

- Source PDF: path, size, timestamp.
- Destination PDF: path, confirmed byte-identical after copy.
- Commit SHA and message used in personal-site.
- Vercel deployment ID and current `readyState`.
- The public URL once it is live: `https://germankuber.com/Germán%20Küber.pdf`
  (note the URL-encoded space; the in-app download button on germankuber.com
  handles encoding itself).

Do not promise that the deploy succeeded until `readyState` is `READY`. If it is
still `BUILDING` at report time, say so.

## What this skill explicitly does NOT do

- Does NOT edit `Resumes/Human/resume.html`. Use `/update-resume` for that.
- Does NOT regenerate the PDF. The user is expected to have done that via
  `npm run pdf` inside `Human/` (or via `/update-resume` Step 6.6) before
  invoking this skill.
- Does NOT touch any of the 9 ATS resume folders.
- Does NOT create branches, open PRs, or do anything beyond push-to-main on
  personal-site. The personal-site repo treats `main` as the deploy branch by
  convention.
