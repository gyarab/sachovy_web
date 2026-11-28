#!/usr/bin/bash
echo "VNVDIR=\"$(pwd)/$1\"" > rc
cat >> rc << EOF
a() {
    source \$VNVDIR/bin/activate
}

alias twcss="npx @tailwindcss/cli"
EOF

source rc
