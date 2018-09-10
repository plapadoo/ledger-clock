let
  bootstrap = import <nixpkgs> { };

  nixpkgs = builtins.fromJSON (builtins.readFile ./nixpkgs.json);

  src = bootstrap.fetchFromGitHub {
    owner = "NixOS";
    repo  = "nixpkgs-channels";
    inherit (nixpkgs) rev sha256;
  };

  pkgs = import src { };

  packageOverrides = self: super: {
    fuzzyfinder = super.buildPythonPackage rec {
      pname  = "fuzzyfinder";
      version = "2.1.0";

      src = self.fetchPypi {
        sha256 = "0jzh68qr9nwgp9zchbzqq0qhihinf27m3iwhcsnyqsw623qqcvf5";
        inherit pname version;
      };

      checkInputs = [ super.pytest ];
    };
  };

  python = pkgs.python3.override { inherit packageOverrides; };
  pythonPkgs = python.pkgs;
in
  pythonPkgs.buildPythonApplication rec {
    name = "ledger-clock";
    version = "1.0";
    src = ./.;
    # So nix-shell contains the Python path
    # shellHook = "export PYTHONPATH=$(pwd):$PYTHONPATH";
    propagatedBuildInputs = [
      pythonPkgs.pyxdg
      pythonPkgs.fuzzyfinder
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
