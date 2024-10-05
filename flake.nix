{
  description = "Python keyboard to MIDI converter";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, app }: {
    packages.x86_64-linux.default = let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in pkgs.mkShell {
      buildInputs = [
        pkgs.python312  # Specify Python 3.12
        pkgs.python312Packages.mido
        pkgs.python312Packages.python-rtmidi
        pkgs.python312Packages.pynput  # Use the correct package for Python 3.12
        pkgs.python312Packages.evdev 
        pkgs.hidapi
        pkgs.usbutils
      ];
    };
  };
}
