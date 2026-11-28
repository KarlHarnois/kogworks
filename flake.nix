{
  description = "kogworks: a factory file synthesizer for Knave repositories";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        knaveVersion = "0.22.0";

        knaveSource = pkgs.fetchCrate {
          pname = "knave";
          version = knaveVersion;
          hash = "sha256-2tR3Z2PYIzOzjZwG5WrRIK1ABjLsAveiffUOHE3rs8c=";
        };

        knave = pkgs.rustPlatform.buildRustPackage {
          pname = "knave";
          version = knaveVersion;
          src = knaveSource;
          cargoLock.lockFile = "${knaveSource}/Cargo.lock";
          doCheck = false;
        };

        knaveCommandantRevision = "811d6dc4558cfdabd10d895e26d3087df1ad03e5";

        knaveCommandantSource = pkgs.fetchgit {
          url = "https://github.com/KarlHarnois/knave-commandant";
          rev = knaveCommandantRevision;
          hash = "sha256-j6jLuOnUHJ0/ppIP2EvMuu+5Dxeti2S+5hjpa+rsB14=";
        };

        ledelintRevision = "67d735e0d9c632fc04508b53d4c42dcd1102e95b";

        ledelintSource = pkgs.fetchgit {
          url = "https://github.com/KarlHarnois/ledelint";
          rev = ledelintRevision;
          hash = "sha256-10RYPOSnMQE826i4NGTInQwSPQ+9rgxtIOBtu3GXOL4=";
        };

        vendoredCrates = pkgs.rustPlatform.importCargoLock {
          lockFile = ./Cargo.lock;
        };

        versionSuffix =
          if self ? shortRev then "-g${self.shortRev}"
          else if self ? dirtyShortRev then "-g${self.dirtyShortRev}"
          else "";

        kogworks = pkgs.stdenv.mkDerivation {
          pname = "kogworks";
          version = "0.1.0${versionSuffix}";
          src = ./.;
          nativeBuildInputs = [ knave pkgs.cargo pkgs.rustc pkgs.rustfmt ];
          buildPhase = ''
            export HOME=$TMPDIR
            export CARGO_HOME=$TMPDIR/cargo
            mkdir -p $CARGO_HOME
            cat > $CARGO_HOME/config.toml <<CONFIG
            [source.crates-io]
            replace-with = "vendored"

            [source.vendored]
            directory = "${vendoredCrates}"

            [net]
            offline = true
            CONFIG
            export XDG_CACHE_HOME=$TMPDIR/xdg-cache
            mkdir -p "$XDG_CACHE_HOME/knave/git"
            cp -r "${knaveCommandantSource}" "$XDG_CACHE_HOME/knave/git/${knaveCommandantRevision}"
            cp -r "${ledelintSource}" "$XDG_CACHE_HOME/knave/git/${ledelintRevision}"
            knave build
          '';
          installPhase = ''
            install -Dm755 target/knave/kogworks/kogworks $out/bin/kogworks
          '';
        };
      in
      {
        packages = {
          default = kogworks;
          inherit knave;
        };

        devShells.default = pkgs.mkShell {
          packages = [ knave pkgs.cargo pkgs.rustc pkgs.rustfmt pkgs.git ];
        };
      });
}
