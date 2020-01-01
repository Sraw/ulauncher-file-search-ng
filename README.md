## This is a fork of original [project](https://github.com/brpaz/ulauncher-file-search), for my personal usage.

The reason why I maintain it as a separated project instead of submit a PR is that I cannot wait for the merging.

This fork is not listed in Ulauncher's extensions website.

# ulauncher-file-search

[![Ulauncher Extension](https://img.shields.io/badge/Ulauncher-Extension-green.svg?style=for-the-badge)](https://ext.ulauncher.io/-/github-brpaz-ulauncher-file-search)
[![GitHub license](https://img.shields.io/github/license/sraw/ulauncher-file-search.svg?style=for-the-badge)](https://github.com/sraw/ulauncher-file-search/blob/master/LICENSE)

> Quick Search files and directories from [Ulauncher](https://ulauncher.io) using [https://github.com/sharkdp/fd](fd).

## Demo

![demo](demo.gif)

## Requirements

- Ulauncher 5+
- Python 3+
- [fd](https://github.com/sharkdp/fd) - A simple, fast and user-friendly alternative to 'find'. Notice you need to install it.

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```
https://github.com/Sraw/ulauncher-file-search
```

## Usage

This extension provides the following keywords:

- fd -> Search files and directories
- ff -> Search Files
- fdir -> Search directories

To search, input one of the previous keywords to trigger the extension and start typing your search criteria. 
Ulauncher will call "fd" under the hood to perform your search and it will display a list of results.

### Result items Actions

- Press "Enter" - Open the file / folder using the default system action
- Press "Alt+Enter" - On a folder, it will open the respective folder in a Terminal window.

### Extension settings

- **Terminal Emulator** -> Sets the terminal emulator to use when opening directories. Default: `gnome-terminal`
- **Base dir** -> The base directory to start your searches as an absolute path. Default: `/`
- **fd command** -> Specify the command of the fd tool. Mostly it should be fd. Default: `fd`
- **Timeout of search** -> Specify a timeout in second for the search action. Default: `5`
- **Threads limitation** -> Specify how many threads to use for the search action. 0 means the same as cores. Default: `0`

## Contributing

Please go to the original [project](https://github.com/brpaz/ulauncher-file-search).

## Links

* [Ulauncher Extensions](https://ext.ulauncher.io/)
* [Ulauncher 5.0 (Extension API v2.0.0) — Ulauncher 5.0.0 documentation](http://docs.ulauncher.io/en/latest/)

## License

MIT &copy; [Bruno Paz](http://brunopaz.net)

MIT &copy; Sraw
