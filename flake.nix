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
        packages.default = self.packages.${system}.${name};
        
        packages.${name} = with import nixpkgs { inherit system; };
          stdenv.mkDerivation {
            src = lib.cleanSource ./.; # self;
            name = "${name}";
            version = "${version}";

            __noChroot = true;
            dontUseCmakeConfigure = true;
            dontPatchELF = false;
            dontFixup = true;
              
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
              rsync
              watchexec
              xz
              zeromq
            ];

            buildPhase = ''
              export HOME=/tmp
              export SHELL=$BASH
              export LANG=en_US.UTF-8
              python3 -m venv .venv
              source .venv/bin/activate
              make conan-install
              make build
            '';

            installPhase = ''
              mkdir -p $out/bin
              cp --archive --preserve --dereference dist3/* $out/.
              cp bexec.sh $out/bin
            '';
          };

        packages.docker = pkgs.dockerTools.buildImage {
          name = "basilisk";
          tag = "latest";
          created = "now";

          copyToRoot = pkgs.buildEnv {
            name = "${name}";
            paths = with pkgs; [
              self.packages.${system}.${name}
              bashInteractive
              cacert
              coreutils
              findutils
              gnugrep
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
            ];
            pathsToLink = [ "/" "/bin" "/etc" ];
          };

          config = {
            WorkingDir = "/";
            Env = [
              "NIX_SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
              "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
              "SYSTEM_CERTIFICATE_PATH=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
              #"PYTHONPATH=/lib/${name}:$PYTHONPATH"
            ];
            EntryPoint = [ "${pkgs.bashInteractive}/bin/bash" ];
            # CMD = [ "change-event" ]; # name of lambda handler
          };
        };

        
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
