# Release Process

How PDF Sentinel releases are created and published.

## Versioning

PDF Sentinel follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 2.0.0)
- **MAJOR:** Breaking changes
- **MINOR:** New features (backwards compatible)
- **PATCH:** Bug fixes (backwards compatible)

## Release Workflow

### 1. Prepare Release

Update version number in:
- `pyproject.toml`
- `src/pdf_sentinel/__init__.py`

Update changelog:
```markdown
## [2.1.0] - 2025-11-15

### Added
- New feature X
- New feature Y

### Fixed
- Bug Z
```

### 2. Create Git Tag

```bash
git tag -a v2.1.0 -m "Release v2.1.0: New features X and Y"
git push origin v2.1.0
```

### 3. GitHub Actions Handles Rest

The [release workflow](.github/workflows/release.yml) automatically:

1. **Builds packages** (wheel + tarball)
2. **Creates GitHub Release** with auto-generated notes
3. **Uploads artifacts** to release

### 4. Verify Release

Check [GitHub Releases](https://github.com/Ai4GenXers/pdf-sentinel/releases):

- ✅ Release created
- ✅ Packages attached (`.whl` and `.tar.gz`)
- ✅ Release notes generated

## Manual Release (If Needed)

### Build Packages

```bash
python -m build
```

Creates:
- `dist/pdf_sentinel-2.1.0-py3-none-any.whl`
- `dist/pdf_sentinel-2.1.0.tar.gz`

### Create GitHub Release

```bash
gh release create v2.1.0 \
  dist/pdf_sentinel-2.1.0-py3-none-any.whl \
  dist/pdf_sentinel-2.1.0.tar.gz \
  --title "v2.1.0" \
  --notes "Release notes here"
```

## PyPI Publication (Future)

When ready to publish to PyPI:

1. **Get PyPI token** from https://pypi.org/manage/account/token/

2. **Add to GitHub Secrets:** `PYPI_API_TOKEN`

3. **Uncomment PyPI section** in `.github/workflows/release.yml`:
   ```yaml
   - name: Publish to PyPI
     env:
       TWINE_USERNAME: __token__
       TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
     run: |
       twine upload dist/*
   ```

4. **Future releases** will auto-publish to PyPI

## Release Checklist

Before creating release:

- [ ] All tests passing
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] README.md accurate
- [ ] Documentation up to date
- [ ] No uncommitted changes

After release:

- [ ] GitHub Release created
- [ ] Packages attached to release
- [ ] Release notes accurate
- [ ] Installation tested from release
- [ ] ReadTheDocs updated (if applicable)

## Hotfix Releases

For urgent bug fixes:

1. Create hotfix branch from tag
2. Apply minimal fix
3. Increment PATCH version
4. Follow normal release process
5. Merge back to main

Example:
```bash
git checkout -b hotfix/2.0.1 v2.0.0
# Apply fix
# Update to 2.0.1
git tag v2.0.1
git push origin v2.0.1
git checkout main
git merge hotfix/2.0.1
```

## Next Steps

- **[Contributing](../contributing.md)** - Contribution guidelines
- **[Testing](testing.md)** - Testing guide
