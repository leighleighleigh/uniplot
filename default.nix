{ pkgs ? import <nixpkgs> {} }:
let
  poetry2nix = pkgs.fetchFromGitHub {
    owner = "nix-community";
    repo = "poetry2nix";
    rev = "e0b44e9e2d3aa855d1dd77b06f067cd0e0c3860d";
    sha256 = "sha256-puYyylgrBS4AFAHeyVRTjTUVD8DZdecJfymWJe7H438=";
  };

  devpkgs = import <nixpkgs> {
    overlays = [ (import "${poetry2nix.outPath}/overlay.nix") ];
  };
in devpkgs.poetry2nix.mkPoetryPackages {
    projectDir = ./.;
    preferWheels = true;
    editablePackageSources = {
        uniplot = ./.;
    };
}
