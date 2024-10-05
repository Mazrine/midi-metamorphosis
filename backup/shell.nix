{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.mido
    pkgs.python3Packages.python-rtmidi
    pkgs.python3Packages.hid
    pkgs.hidapi
    pkgs.usbutils
  ];
}
