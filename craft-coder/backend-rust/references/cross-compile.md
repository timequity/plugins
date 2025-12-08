# Cross-Compilation

## Common Targets

| Target | Platform | Use Case |
|--------|----------|----------|
| `x86_64-unknown-linux-gnu` | Linux x64 | Standard Linux servers |
| `x86_64-unknown-linux-musl` | Linux x64 (static) | Alpine, containers, portable |
| `aarch64-unknown-linux-gnu` | Linux ARM64 | AWS Graviton, Raspberry Pi 4 |
| `aarch64-unknown-linux-musl` | Linux ARM64 (static) | ARM containers |
| `x86_64-pc-windows-gnu` | Windows x64 | Cross from Linux/Mac |
| `x86_64-pc-windows-msvc` | Windows x64 | Native Windows |
| `x86_64-apple-darwin` | macOS x64 | Intel Macs |
| `aarch64-apple-darwin` | macOS ARM64 | M1/M2/M3 Macs |

## Setup

### Install Target

```bash
rustup target add x86_64-unknown-linux-musl
rustup target list --installed
```

### Install Linker (musl)

```bash
# Ubuntu/Debian
apt-get install musl-tools

# macOS
brew install filosottile/musl-cross/musl-cross

# Configure linker in .cargo/config.toml
[target.x86_64-unknown-linux-musl]
linker = "x86_64-linux-musl-gcc"
```

### Install Linker (ARM64)

```bash
# Ubuntu/Debian
apt-get install gcc-aarch64-linux-gnu

# Configure
[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```

## Build

```bash
# Simple cross-compile
cargo build --release --target x86_64-unknown-linux-musl

# With script
python scripts/build.py --release --target x86_64-unknown-linux-musl
```

## Using cross (Docker-based)

Cross uses Docker containers for cross-compilation. No local toolchains needed.

```bash
# Install
cargo install cross

# Build
cross build --release --target x86_64-unknown-linux-musl
cross build --release --target aarch64-unknown-linux-gnu
```

### Cross.toml Configuration

```toml
[build.env]
passthrough = ["RUST_BACKTRACE", "DATABASE_URL"]

[target.x86_64-unknown-linux-musl]
image = "ghcr.io/cross-rs/x86_64-unknown-linux-musl:main"
```

## Cargo Configuration

### .cargo/config.toml

```toml
[build]
# Default target for cargo build
target = "x86_64-unknown-linux-musl"

[target.x86_64-unknown-linux-musl]
linker = "x86_64-linux-musl-gcc"
rustflags = ["-C", "target-feature=+crt-static"]

[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```

## Release Profile

### Cargo.toml

```toml
[profile.release]
lto = true           # Link-time optimization
codegen-units = 1    # Better optimization, slower compile
strip = true         # Strip symbols
panic = "abort"      # Smaller binary
opt-level = "z"      # Optimize for size (or "3" for speed)
```

### Size Comparison

| Option | Binary Size | Build Time |
|--------|-------------|------------|
| Default | ~10 MB | Fast |
| LTO + strip | ~3 MB | Slow |
| opt-level = "z" | ~2 MB | Slow |
| + upx --best | ~800 KB | Very slow |

## Troubleshooting

### OpenSSL Issues

```toml
# Cargo.toml - use rustls instead of openssl
[dependencies]
reqwest = { version = "0.11", default-features = false, features = ["rustls-tls"] }
```

### C Dependencies

For crates with C dependencies, cross or Docker is often easier than setting up local toolchains.

### Static Linking

```bash
# Ensure static linking with musl
RUSTFLAGS="-C target-feature=+crt-static" cargo build --release --target x86_64-unknown-linux-musl
```
