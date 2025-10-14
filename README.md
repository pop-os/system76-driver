# System76 Driver

This program installs drivers and provides restore functionality for System76
machines.

Open Activities button on the top left or use the Ubuntu/Pop!\_OS/Super key and
search for 'system76' then click the icon and enter your password to open the
application.

## Making changes

1. Checkout new branch
2. Make changes
3. Bump the version in `system76driver/__init__.py`
4. Update `debian/changelog` using debchange
5. Make a pull request

## Making a release

1. Pull the latest changes for `master`
2. Create a signed tag using the version as the name
3. Push the tag

```
git checkout master
git pull
git tag -s <VERSION>
git push origin tag <VERSION>
```

## License

This software is made available under the terms of the GNU General Public
License; either version 2 of the License, or (at your option) any later
version. See [LICENSE](LICENSE) for details.
