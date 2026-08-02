#!/usr/bin/env python3
"""Verifica se todo link relativo dos arquivos .md aponta para um arquivo real.

A reorganizacao de pastas e a causa mais comum de link quebrado neste
repositorio. Este script roda no CI e falha se algum alvo nao existir.

Links externos ficam de fora. Um site fora do ar deixaria o resultado
vermelho sem nenhuma culpa do repositorio.

Uso: python3 .github/scripts/check_links.py
"""

import re
import sys
from pathlib import Path

# Casa [texto](alvo) e ![texto](alvo). O ancora depois de # e descartado,
# porque o alvo em disco nao depende dele.
LINK = re.compile(r"!?\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")

EXTERNO = ("http://", "https://", "mailto:", "#")

# Pastas que nao contem documentacao do repositorio.
IGNORAR = {".git"}


def main() -> int:
    raiz = Path(__file__).resolve().parents[2]
    quebrados: list[str] = []
    total = 0

    for md in sorted(raiz.rglob("*.md")):
        if any(parte in IGNORAR for parte in md.parts):
            continue

        texto = md.read_text(encoding="utf-8", errors="replace")

        for achado in LINK.finditer(texto):
            alvo = achado.group(1).strip()
            if alvo.startswith(EXTERNO):
                continue

            total += 1
            if not (md.parent / alvo).exists():
                relativo = md.relative_to(raiz)
                quebrados.append(f"  {relativo} -> {alvo}")

    if quebrados:
        print(f"Links relativos quebrados: {len(quebrados)} de {total}\n")
        print("\n".join(quebrados))
        return 1

    print(f"OK. Os {total} links relativos apontam para arquivos existentes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
