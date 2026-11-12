# Second Nature

*Kisi bhi AI agent ke liye aapka kaam karne ka tareeka second nature: skills, memory, rules.*

### 30 skills, 300 nahi

**Product banane ke har padaav ke liye ek tested agent skill: "ye idea chalega?" se launch tak.**
Claude Code, Codex, Cursor, Gemini CLI, opencode, aur har us agent me chalta hai jo `SKILL.md` padhta hai.

[English README](README.md)

## Ye kyun bana

Mere laptop pe 280 skills installed thi. Maine un pe health check chalaya:

- **11 skills chal hi nahi sakti thi** (dependency missing).
- **4 jodi skills ka naam ek jaisa tha**, to kaun si load hogi ye kismat thi.
- **39 alag skills "design" shabd pe jaag jaati thi.** Agent ko har baar inme se chunna padta tha, aur chunne ke liye
  wo har skill ka description padhta hai.

Zyada skills ka matlab: zyada token, aur zyada baar galat skill. To maine ulta kiya: GitHub chhaana, har padaav ki
**ek** sabse achhi skill rakhi, har ek ko asli project pe chalaya, aur apni skill sirf wahan likhi jahan
mojooda skills ek doosre ki nakal thi ya koi thi hi nahi.

## Install (30 second)

```bash
npx skills@latest add anki1kr/second-nature
```

Node nahi hai?

```bash
git clone https://github.com/anki1kr/second-nature && cd second-nature
bash install.sh --recommended        # Windows PowerShell: .\install.ps1 -Recommended
```

Phir apne agent se poocho: *"idea validate karne ke liye mere paas kaun si skill hai?"*

## Kya milta hai

- **9 skills is repo me**: idea-truth, decide, design-review, search-visibility, launch-legal (EU GDPR, UK, US California, India DPDP),
  hackathon-agent, orchestrate, update-mem, skills-doctor.
- **21 linked skills**: har padaav ki best skill, uske asli author ke repo se, bina badle. Poori list aur license:
  [CREDITS.md](CREDITS.md). Padaav-wise table: [README.md](README.md#the-30-by-stage).
- **Memory vault**: har session me bahut kam load hota hai, baaki zaroorat pe local search se milta hai.
  [Kaise kaam karta hai](docs/memory-system.md).

## Kya test hua

Har daave ki report [`reports/`](reports) me hai. Poori table English README me hai. Jo saabit nahi hua wo bhi wahin
likha hai: ye skills model ko "smart" banati hain, aisa maine naapa nahi hai; aur `launch-legal` kanooni salah nahi hai.

MIT license. Banaya [anki1kr](https://github.com/anki1kr) ne.
