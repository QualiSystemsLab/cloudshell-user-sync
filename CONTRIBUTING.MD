## Testing

- [pytest](https://docs.pytest.org) as the default test runner
- [Tox](https://tox.readthedocs.io) to manage test environments
- Include tests with pull requests

## Pre-commit and Linting

- Use [pre-commit](https://pre-commit.com/) as the lint and formatter runner
- See `.pre-commit-config.yaml` file for hook settings and lint rules
- Used both locally and in Github Actions CI

Formatter / Linter hooks:

- [Black Formatter](https://github.com/psf/black) 
- [Flake8 Linter](https://flake8.pycqa.org/en/latest/) 
- [Pylint Linter](https://pypi.org/project/pylint/)

Install pre-commit and all dev dependencies

```commandline
pip install requirements-dev.txt
```

run pre-commit for all files ad-hoc

```commandline
pre-commit run -a
```

commit and skip pre-commit action

```commandline
git commit -m "my commit message" --no-verify
```

## Release / CI

- Some default Github Actions workflows for linting and release packaging are included.
- Pushes to all branches and merge to master / main triggers linting workflow.
- Pushing tags that start with "v" will kick off release workflow.

#### Sample Release Flow

- Merge feature branch pull request into main / master
- On local machine, check out main / master
- `git pull` remote changes
- Use [Bump2version](https://pypi.org/project/bump2version/) to bump `version.txt` and create matching "v" release tag.
- `git push` the annotated tag to remote, which kicks off the release CI flow

bump2version command:
```commandline
bump2version patch --tag-message "fixed some bugs in this release"
```
- major / minor / patch will update the respective parts of a SEMVER release (Major.Minor.Patch)
- This command is abbreviated, and relies on `.bumpversion.cfg` to define target files, and auto-commit / tag behavior

git push bumped version files and annotated tag
```commandline
git push --atomic origin master v0.1.0
```

#### Prune Local Branches
- After merging pull request and deleting branches, clean up local branches.
- Utility npm package, [git-removed-branches](https://www.npmjs.com/package/git-removed-branches) to help with this.

install:
```commandline
npm install -g git-removed-branches
```

use:
```commandline
git checkout main
git fetch -p
git removed-branches --prune
```
