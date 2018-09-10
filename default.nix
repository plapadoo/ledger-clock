let
  bootstrap = import <nixpkgs> { };

  nixpkgs = builtins.fromJSON (builtins.readFile ./nixpkgs.json);

  src = bootstrap.fetchFromGitHub {
    owner = "NixOS";
    repo  = "nixpkgs-channels";
    inherit (nixpkgs) rev sha256;
  };

  pkgs = import src { };

  pythonPkgs = pkgs.python3Packages;
in
  pythonPkgs.buildPythonApplication rec {
    name = "ledger-clock";
    version = "1.0";
    src = ./.;
    # So nix-shell contains the Python path
    # shellHook = "export PYTHONPATH=$(pwd):$PYTHONPATH";
    propagatedBuildInputs = [
      pythonPkgs.pyxdg
    ];
    # checkPhase = ''
    #   PYLINTHOME="/tmp" pylint ledger_jira_sync
    # '';
    # checkInputs = [ pythonPkgs.pylint ];

    buildInputs = [
      pkgs.python3
      pythonPkgs.ipython
      pythonPkgs.pylint
      pythonPkgs.mypy
      pythonPkgs.yapf
    ];
}
