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

  repoSrc = ./.;

  ledger-clock = pythonPkgs.buildPythonApplication rec {
    name = "ledger-clock";
    version = "1.0";
    src = repoSrc;
    propagatedBuildInputs = [
      pythonPkgs.pyxdg
      pythonPkgs.fuzzyfinder
    ];
    checkPhase = ''
      PYLINTHOME="/tmp" pylint ledgerclock
      mypy ledgerclock
    '';
    checkInputs = [ pythonPkgs.pylint pythonPkgs.mypy ];

    buildInputs = [
      pkgs.python3
      pythonPkgs.ipython
      pythonPkgs.pylint
      pythonPkgs.mypy
      pythonPkgs.yapf
    ];
  };
in
  pkgs.stdenv.mkDerivation rec {
    name = "ledger-clock-helpers-${version}";
    version = "1.0";
    src = repoSrc;

    buildInputs = [ ledger-clock pkgs.rofi pkgs.libnotify ];

    #phases = [ "patchPhase" "unpackPhase" "installPhase" ];
    patchPhase = ''
      substituteInPlace ledger-rofi-start-clock.sh --replace 'ledgerclock_bin=ledgerclock' ledgerclock_bin=${ledger-clock}/bin/ledgerclock
      substituteInPlace ledger-rofi-start-clock.sh --replace 'rofi_bin=rofi' rofi_bin=${pkgs.rofi}/bin/rofi
      substituteInPlace ledger-rofi-start-clock.sh --replace 'notify_bin=notify-send' notify_bin=${pkgs.libnotify}/bin/notify-send

      substituteInPlace ledger-rofi-stop-clock.sh --replace 'ledgerclock_bin=ledgerclock' ledgerclock_bin=${ledger-clock}/bin/ledgerclock
      substituteInPlace ledger-rofi-stop-clock.sh --replace 'rofi_bin=rofi' rofi_bin=${pkgs.rofi}/bin/rofi
      substituteInPlace ledger-rofi-stop-clock.sh --replace 'notify_bin=notify-send' notify_bin=${pkgs.libnotify}/bin/notify-send

      substituteInPlace commit-clocks.sh --replace 'ledgerclock_bin=ledgerclock' ledgerclock_bin=${ledger-clock}/bin/ledgerclock
      substituteInPlace commit-clocks.sh --replace 'notify_bin=notify-send' notify_bin=${pkgs.libnotify}/bin/notify-send
    '';

    installPhase = ''
      mkdir -p $out/bin
      cp ledger-rofi-start-clock.sh $out/bin
      cp ledger-rofi-stop-clock.sh $out/bin
      cp commit-clocks.sh $out/bin
    '';
  }
