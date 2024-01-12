{
  description = "basilisk: an astrodynamics simulator framework";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        name = "basilisk";
        version = "0.1.0";
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            bashInteractive
            cmake
            cmakeCurses
            #conan
            coreutils
            findutils
            git
            gnugrep
            gnumake
            gnused
            python3
            python3.pkgs.colorama
            python3.pkgs.matplotlib
            python3.pkgs.numpy
            python3.pkgs.pandas
            python3.pkgs.parse
            python3.pkgs.pillow
            python3.pkgs.pip
            python3.pkgs.pytest
            python3.pkgs.pytest-xdist
            python3.pkgs.setuptools
            python3.pkgs.tkinter
            python3.pkgs.tqdm
            python3.pkgs.urllib3
            python3.pkgs.virtualenv
            python3.pkgs.wheel
            sourceHighlight
            swig4
            watchexec
            zlib
          ];

          shellHook = ''
            export SHELL=$BASH
            export LANG=en_US.UTF-8
            export PYTHONPATH=$PWD/dist3:$PYTHONPATH
            export PS1="nix|$PS1"
            python3 -m venv .venv
            source .venv/bin/activate
          '';
        };

        devShell = self.devShells.${system}.default;
      }
    );
}
