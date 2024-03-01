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
        nixConfig.sandbox = false; # "relaxed";           
      in {
        packages.${name} = with import nixpkgs { inherit system; };
          stdenv.mkDerivation {
            __noChroot = true;
            name = "${name}";
            src = self;
            version = "${version}";
            dontUseCmakeConfigure = true;

            buildInputs = with pkgs; [
              cmake
              cmakeCurses
              #conan
              coreutils
              cppzmq
              eigen
              jasper
              findutils
              gnugrep
              gnumake
              gnused
              libjpeg
              libpng
              libwebp
              opencv
              pcre
              pkg-config
              protobuf
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
              xz
              zeromq
              swig4
            ];

            buildPhase = ''
              export HOME=$out
              export SHELL=$BASH
              export LANG=en_US.UTF-8
              export PYTHONPATH=$PWD/dist3:$PYTHONPATH

              python3 -m venv .venv
              source .venv/bin/activate
              make install-conan
              make build                                          
            '';
            installPhase = ''
              ls -l $out
            '';
          };
        packages.default = self.packages.${system}.${name};
        defaultPackage = self.packages.${system}.default;
        
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            bashInteractive
            cmake
            cmakeCurses
            #conan
            coreutils
            cppzmq
            eigen
            jasper
            findutils
            git
            gnugrep
            gnumake
            gnused
            libjpeg
            libpng
            libwebp
            opencv
            pcre
            pkg-config
            protobuf
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
            xz
            zeromq
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
      }
    );
}
