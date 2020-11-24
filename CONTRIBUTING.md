# Contributing

Looking to contribute something to Lab Dashboard? Here's how you can help.

## Lab Dashboard

Do you want to help us to improve lab dashboard ?

### Key Branch

- `main` is the latest, deployed version

### Create Issue

We only accept issues that bug reports or feature requests.

* [Request a new feature](https://github.com/suam-team/lab-dashboard/issues/new?title=Feature%20request:feature-name)
* [Submit a bug report](https://github.com/suam-team/lab-dashboard/issues/new?title=Bug%Report:bug-title)

### Pull Request

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md or .env.example files (if any).

## Hacking Lab

Do you want to add your lab to lab dashboard ?h

### Lab Specification

- The lab must store in the Github public repo.
- The `lab.json` must be added to the root path of Github repo ([Example](https://github.com/suam-team/ctr-broken-couter-lab/blob/main/lab.json)).
  - `name`: Lab name
  - `category`: Lab category
  - `author`: Your name
  - `flag`: Leaving it blank
  - `detail`: Lab detail
- If a server is required, please make your lab to be deployable in heroku platform.
- The application must read the flag from `FLAG` environment (please do not hard-coded the flag in your source code).
- Please add the deploy step to the README.md file.
- The lab's license must be the MIT License [https://github.com/git/git-scm.com/blob/master/MIT-LICENSE.txt](https://github.com/git/git-scm.com/blob/master/MIT-LICENSE.txt).

### Notify Us

You can submit your lab to us by sending it to [lab@suam.wtf](mailto:lab@suam.wtf) email or tell us in the discord ([ComSci_TH](https://discord.gg/tufqH4m)). The Github repo URL, correct flag, and breif solution must be included.

### Hacking Lab Example

* [https://github.com/suam-team/ctr-broken-couter-lab](https://github.com/suam-team/ctr-broken-couter-lab)
* [https://github.com/suam-team/ctr-static-nonce-lab](https://github.com/suam-team/ctr-static-nonce-lab)