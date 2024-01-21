{ pkgs ? import <nixpkgs> {} }:
let
  uniplot = pkgs.callPackage ./default.nix {inherit pkgs;};
in pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    (pkgs.python3.withPackages(ps: [] ++ uniplot.poetryPackages))
  ];
}
