"""
Script para gerar diagramas de alta qualidade para apresentacao sobre Sharding.
Gera os diagramas como PNG de alta resolucao.

Uso: python generate_diagrams.py
Requer: matplotlib, numpy, pillow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow, FancyArrowPatch
from matplotlib.patches import ConnectionPatch
import matplotlib.lines as mlines
import numpy as np
from collections import defaultdict
import hashlib
import os

# Configuracao de estilo global
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['figure.dpi'] = 150

# Cores do tema
COLORS = {
    'primary': '#3498db',      # Azul
    'secondary': '#2ecc71',    # Verde
    'accent': '#e74c3c',       # Vermelho
    'warning': '#f39c12',      # Laranja
    'purple': '#9b59b6',       # Roxo
    'dark': '#2c3e50',         # Cinza escuro
    'light': '#ecf0f1',        # Cinza claro
    'bg_mono': '#e3f2fd',      # Fundo azul claro
    'bg_shard': '#e8f5e9',     # Fundo verde claro
}


def save_figure(fig, filename, dpi=150):
    """Salva a figura em alta resolucao."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"OK: Salvo: {filepath}")
    plt.close(fig)


# =============================================================================
# DIAGRAMA 1: Escala Vertical vs. Horizontal
# =============================================================================
def create_scaling_comparison():
    """Cria diagrama comparando escalabilidade vertical vs horizontal."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # --- ESCALA VERTICAL ---
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('ESCALABILIDADE VERTICAL\n(Scale Up)', fontsize=14, fontweight='bold', color=COLORS['primary'])
    
    # Servidor original pequeno
    rect1 = FancyBboxPatch((1.5, 2), 2, 3, boxstyle="round,pad=0.1", 
                           facecolor=COLORS['light'], edgecolor=COLORS['primary'], linewidth=2)
    ax1.add_patch(rect1)
    ax1.text(2.5, 3.5, '[SERVER]\n4 CPU\n8 GB RAM', ha='center', va='center', fontsize=9)
    
    # Seta de upgrade
    ax1.annotate('', xy=(5.5, 3.5), xytext=(4, 3.5),
                arrowprops=dict(arrowstyle='->', lw=3, color=COLORS['warning']))
    ax1.text(4.75, 4.5, 'UPGRADE', ha='center', fontsize=10, color=COLORS['warning'], fontweight='bold')
    ax1.text(4.75, 4.0, '(Alto Custo)', ha='center', fontsize=9, color=COLORS['warning'])
    
    # Servidor maior
    rect2 = FancyBboxPatch((6, 1.5), 3, 4, boxstyle="round,pad=0.1",
                           facecolor=COLORS['bg_mono'], edgecolor=COLORS['primary'], linewidth=3)
    ax1.add_patch(rect2)
    ax1.text(7.5, 3.5, '[SERVER]\n32 CPU\n128 GB RAM', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Limites
    ax1.text(5, 7.5, '[ATENCAO] Limites Fisicos', ha='center', fontsize=12, color=COLORS['accent'], fontweight='bold')
    ax1.text(5, 6.8, '- Hardware tem teto maximo', ha='center', fontsize=10, color='gray')
    ax1.text(5, 6.2, '- Downtime durante upgrade', ha='center', fontsize=10, color='gray')
    
    # --- ESCALA HORIZONTAL ---
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('ESCALABILIDADE HORIZONTAL\n(Scale Out - Sharding)', fontsize=14, fontweight='bold', color=COLORS['secondary'])
    
    # Servidores multiplos
    servers = [(0.5, 2), (3.5, 2), (6.5, 2)]
    for i, (x, y) in enumerate(servers):
        rect = FancyBboxPatch((x, y), 2.5, 3, boxstyle="round,pad=0.1",
                              facecolor=COLORS['bg_shard'], edgecolor=COLORS['secondary'], linewidth=2)
        ax2.add_patch(rect)
        ax2.text(x+1.25, y+1.5, f'[SERVER]\nShard {i+1}', ha='center', va='center', fontsize=10)
    
    # Adicionar novo servidor
    ax2.annotate('', xy=(9, 3.5), xytext=(8.5, 3.5),
                arrowprops=dict(arrowstyle='->', lw=3, color=COLORS['secondary']))
    ax2.text(9.3, 3.5, '+', ha='center', fontsize=24, va='center', fontweight='bold', color=COLORS['secondary'])
    ax2.text(9.3, 2.3, '+ Shard', ha='center', fontsize=9)
    
    # Beneficios
    ax2.text(5, 7.5, '[OK] Sem Limites Teoricos', ha='center', fontsize=12, color=COLORS['secondary'], fontweight='bold')
    ax2.text(5, 6.8, '- Adicione nos conforme necessario', ha='center', fontsize=10, color='gray')
    ax2.text(5, 6.2, '- Sem downtime (hot add)', ha='center', fontsize=10, color='gray')
    
    plt.tight_layout()
    save_figure(fig, '01_escala_vertical_vs_horizontal.png')


# =============================================================================
# DIAGRAMA 2: Comparacao Sharding vs Particionamento vs Replicacao
# =============================================================================
def create_concept_comparison():
    """Cria diagrama visual comparando os tres conceitos."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    
    concepts = [
        {
            'title': 'PARTICIONAMENTO',
            'subtitle': '(Mesmo Servidor)',
            'color': COLORS['primary'],
            'desc': ['Divide dados', 'em partes', 'NO MESMO', 'servidor']
        },
        {
            'title': 'SHARDING',
            'subtitle': '(Multiplos Servidores)',
            'color': COLORS['secondary'],
            'desc': ['Distribui dados', 'entre DIFERENTES', 'servidores', 'independentes']
        },
        {
            'title': 'REPLICACAO',
            'subtitle': '(Copias Identicas)',
            'color': COLORS['purple'],
            'desc': ['Copia dados', 'completos para', 'multiplos', 'servidores']
        }
    ]
    
    for ax, concept in zip(axes, concepts):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Titulo
        ax.text(5, 9.2, concept['title'], ha='center', fontsize=14, fontweight='bold', color=concept['color'])
        ax.text(5, 8.4, concept['subtitle'], ha='center', fontsize=10, color='gray')
        
        # Visualizacao especifica
        if concept['title'] == 'PARTICIONAMENTO':
            # Um servidor grande dividido
            rect = FancyBboxPatch((2, 2), 6, 4.5, boxstyle="round,pad=0.1",
                                  facecolor=COLORS['light'], edgecolor=concept['color'], linewidth=3)
            ax.add_patch(rect)
            # Divisoes internas
            ax.plot([5, 5], [2, 6.5], color=concept['color'], linewidth=2, linestyle='--')
            ax.plot([2, 8], [4.25, 4.25], color=concept['color'], linewidth=2, linestyle='--')
            ax.text(3.5, 5.25, 'Part 1', ha='center', fontsize=9)
            ax.text(6.5, 5.25, 'Part 2', ha='center', fontsize=9)
            ax.text(3.5, 3.25, 'Part 3', ha='center', fontsize=9)
            ax.text(6.5, 3.25, 'Part 4', ha='center', fontsize=9)
            ax.text(5, 1.2, '1 Servidor', ha='center', fontsize=11, fontweight='bold')
            
        elif concept['title'] == 'SHARDING':
            # Multiplos servidores independentes
            positions = [(1.5, 3.5), (4, 3.5), (6.5, 3.5)]
            for i, (x, y) in enumerate(positions):
                rect = FancyBboxPatch((x, y), 2, 2.5, boxstyle="round,pad=0.1",
                                      facecolor=COLORS['bg_shard'], edgecolor=concept['color'], linewidth=2)
                ax.add_patch(rect)
                ax.text(x+1, y+1.25, f'S{i+1}\n[DB]', ha='center', va='center', fontsize=10)
            ax.text(5, 1.2, '3 Servidores', ha='center', fontsize=11, fontweight='bold')
            
        else:  # Replicacao
            # Um master e copias
            positions = [(1.5, 3.5), (4, 3.5), (6.5, 3.5)]
            labels = ['Master', 'Replica', 'Replica']
            for (x, y), label in zip(positions, labels):
                rect = FancyBboxPatch((x, y), 2, 2.5, boxstyle="round,pad=0.1",
                                      facecolor='#fce4ec' if label == 'Master' else COLORS['light'],
                                      edgecolor=concept['color'], linewidth=2)
                ax.add_patch(rect)
                ax.text(x+1, y+1.25, f'{label}\n[DB]', ha='center', va='center', fontsize=9)
            ax.text(5, 1.2, 'Dados Identicos', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, '02_sharding_vs_particionamento_vs_replicacao.png')


# =============================================================================
# DIAGRAMA 3: Arquitetura Monolitica vs Sharded
# =============================================================================
def create_architecture_comparison():
    """Cria diagrama de arquitetura monolitica vs sharded."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    
    # --- MONOLITICO ---
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 12)
    ax1.axis('off')
    ax1.set_title('ARQUITETURA MONOLITICA', fontsize=14, fontweight='bold', color=COLORS['primary'])
    
    # Aplicacao
    app1 = FancyBboxPatch((3, 9), 4, 1.5, boxstyle="round,pad=0.1",
                          facecolor='#fff3e0', edgecolor=COLORS['warning'], linewidth=2)
    ax1.add_patch(app1)
    ax1.text(5, 9.75, '[APP] Aplicacao', ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Seta
    ax1.annotate('', xy=(5, 7.3), xytext=(5, 8.8),
                arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['dark']))
    
    # Banco unico
    db1 = FancyBboxPatch((2, 3), 6, 4, boxstyle="round,pad=0.1",
                         facecolor=COLORS['bg_mono'], edgecolor=COLORS['primary'], linewidth=3)
    ax1.add_patch(db1)
    ax1.text(5, 5.5, '[DATABASE]', ha='center', fontsize=14, fontweight='bold')
    ax1.text(5, 4.5, 'Banco Unico\n(Todos os Dados)', ha='center', va='center', fontsize=11)
    
    # Problema
    ax1.text(5, 1.5, '[!] Gargalo unico\n[!] Limite de escala', ha='center', fontsize=10, color=COLORS['accent'])
    
    # --- SHARDED ---
    ax2 = axes[1]
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 12)
    ax2.axis('off')
    ax2.set_title('ARQUITETURA SHARDED', fontsize=14, fontweight='bold', color=COLORS['secondary'])
    
    # Aplicacao
    app2 = FancyBboxPatch((4, 10), 4, 1.2, boxstyle="round,pad=0.1",
                          facecolor='#fff3e0', edgecolor=COLORS['warning'], linewidth=2)
    ax2.add_patch(app2)
    ax2.text(6, 10.6, '[APP] Aplicacao', ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Query Router
    router = FancyBboxPatch((4, 7.5), 4, 1.5, boxstyle="round,pad=0.1",
                            facecolor='#fff3e0', edgecolor=COLORS['warning'], linewidth=2)
    ax2.add_patch(router)
    ax2.text(6, 8.25, '[ROUTER] Query Router', ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Seta app -> router
    ax2.annotate('', xy=(6, 9.1), xytext=(6, 9.9),
                arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['dark']))
    
    # Config Server
    config = FancyBboxPatch((9.5, 7.5), 2, 1.5, boxstyle="round,pad=0.1",
                            facecolor='#fce4ec', edgecolor=COLORS['accent'], linewidth=2)
    ax2.add_patch(config)
    ax2.text(10.5, 8.25, '[CONFIG]\nMetadata', ha='center', va='center', fontsize=9)
    
    # Seta router -> config (pontilhada)
    ax2.annotate('', xy=(9.4, 8.25), xytext=(8.1, 8.25),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=COLORS['accent'], linestyle='dashed'))
    
    # Shards
    shards_info = [
        (0.5, 2.5, 'Shard 1\nUsers A-H'),
        (4, 2.5, 'Shard 2\nUsers I-P'),
        (7.5, 2.5, 'Shard 3\nUsers Q-Z')
    ]
    
    for x, y, label in shards_info:
        shard = FancyBboxPatch((x, y), 3, 3.5, boxstyle="round,pad=0.1",
                               facecolor=COLORS['bg_shard'], edgecolor=COLORS['secondary'], linewidth=2)
        ax2.add_patch(shard)
        ax2.text(x+1.5, y+2.5, '[DB]', ha='center', fontsize=12, fontweight='bold')
        ax2.text(x+1.5, y+1.2, label, ha='center', va='center', fontsize=9)
    
    # Setas router -> shards
    for x in [2, 5.5, 9]:
        ax2.annotate('', xy=(x, 6.2), xytext=(6, 7.4),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color=COLORS['secondary']))
    
    # Beneficios
    ax2.text(6, 0.8, '[OK] Carga distribuida  [OK] Escala linear', ha='center', fontsize=10, color=COLORS['secondary'])
    
    plt.tight_layout()
    save_figure(fig, '03_arquitetura_monolitica_vs_sharded.png')


# =============================================================================
# DIAGRAMA 4: Estrategias de Particionamento
# =============================================================================
def create_partitioning_strategies():
    """Cria diagrama comparando estrategias de particionamento."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 7))
    
    strategies = [
        {
            'title': 'HASH-BASED',
            'formula': 'shard = hash(key) % N',
            'color': COLORS['primary'],
            'pros': ['[+] Distribuicao uniforme', '[+] Previsivel'],
            'cons': ['[-] Range queries ruins', '[-] Resharding caro']
        },
        {
            'title': 'RANGE-BASED',
            'formula': 'shard = range(key)',
            'color': COLORS['secondary'],
            'pros': ['[+] Range queries OK', '[+] Dados ordenados'],
            'cons': ['[-] Risco de hotspots', '[-] Desbalanceamento']
        },
        {
            'title': 'DIRECTORY-BASED',
            'formula': 'shard = lookup(key)',
            'color': COLORS['purple'],
            'pros': ['[+] Flexivel', '[+] Controle total'],
            'cons': ['[-] Ponto de falha', '[-] Latencia extra']
        }
    ]
    
    for ax, strat in zip(axes, strategies):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Titulo
        ax.text(5, 11.2, strat['title'], ha='center', fontsize=16, fontweight='bold', color=strat['color'])
        ax.text(5, 10.4, strat['formula'], ha='center', fontsize=10, family='monospace', 
                bbox=dict(boxstyle='round', facecolor=COLORS['light']))
        
        # Visualizacao
        if strat['title'] == 'HASH-BASED':
            # Entrada
            ax.text(2, 8.5, 'user_123', ha='center', fontsize=10, family='monospace')
            ax.annotate('', xy=(4, 8.5), xytext=(3.2, 8.5),
                       arrowprops=dict(arrowstyle='->', lw=2))
            # Hash
            hash_box = FancyBboxPatch((4, 8), 2, 1, boxstyle="round,pad=0.05",
                                      facecolor=COLORS['bg_mono'], edgecolor=strat['color'], linewidth=2)
            ax.add_patch(hash_box)
            ax.text(5, 8.5, '#hash', ha='center', fontsize=9)
            ax.annotate('', xy=(7, 8.5), xytext=(6.2, 8.5),
                       arrowprops=dict(arrowstyle='->', lw=2))
            ax.text(8, 8.5, 'Shard 2', ha='center', fontsize=10, color=strat['color'], fontweight='bold')
            
        elif strat['title'] == 'RANGE-BASED':
            # Tabela de ranges
            ranges = [('A-H', 'Shard 1'), ('I-P', 'Shard 2'), ('Q-Z', 'Shard 3')]
            for i, (r, s) in enumerate(ranges):
                y = 8.5 - i*0.8
                ax.text(3.5, y, r, ha='center', fontsize=10)
                ax.text(4.5, y, '->', ha='center', fontsize=10)
                ax.text(6, y, s, ha='center', fontsize=10, color=strat['color'])
            
        else:  # Directory
            # Lookup table
            lookup = FancyBboxPatch((3, 7.5), 4, 2.2, boxstyle="round,pad=0.1",
                                    facecolor='#fce4ec', edgecolor=strat['color'], linewidth=2)
            ax.add_patch(lookup)
            ax.text(5, 9.2, '[LOOKUP TABLE]', ha='center', fontsize=10, fontweight='bold')
            ax.text(5, 8.3, 'key1 -> Shard 2', ha='center', fontsize=9, family='monospace')
            ax.text(5, 7.8, 'key2 -> Shard 1', ha='center', fontsize=9, family='monospace')
        
        # Shards
        for i in range(3):
            x = 1.5 + i * 2.8
            shard = FancyBboxPatch((x, 3), 2, 2.5, boxstyle="round,pad=0.1",
                                   facecolor=COLORS['bg_shard'], edgecolor=strat['color'], linewidth=2)
            ax.add_patch(shard)
            ax.text(x+1, 4.25, f'[DB]\nS{i+1}', ha='center', va='center', fontsize=10)
        
        # Pros e Contras
        y_pos = 2.2
        for pro in strat['pros']:
            ax.text(5, y_pos, pro, ha='center', fontsize=9, color=COLORS['secondary'])
            y_pos -= 0.5
        for con in strat['cons']:
            ax.text(5, y_pos, con, ha='center', fontsize=9, color=COLORS['accent'])
            y_pos -= 0.5
    
    plt.tight_layout()
    save_figure(fig, '04_estrategias_particionamento.png')


# =============================================================================
# DIAGRAMA 5: Consistent Hashing Ring
# =============================================================================
def create_consistent_hashing():
    """Cria visualizacao do Consistent Hashing com Virtual Nodes."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # --- HASH RING ---
    ax1 = axes[0]
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('ANEL DE HASH CONSISTENTE', fontsize=14, fontweight='bold')
    
    # Desenha o anel
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(np.cos(theta), np.sin(theta), 'gray', linewidth=3, alpha=0.3)
    
    # Nos no anel
    node_positions = [30, 120, 210, 300]  # graus
    node_colors = [COLORS['accent'], COLORS['primary'], COLORS['secondary'], COLORS['purple']]
    node_names = ['No A', 'No B', 'No C', 'No D']
    
    for pos, color, name in zip(node_positions, node_colors, node_names):
        rad = np.radians(pos)
        x, y = np.cos(rad), np.sin(rad)
        circle = Circle((x, y), 0.12, facecolor=color, edgecolor='white', linewidth=2, zorder=5)
        ax1.add_patch(circle)
        ax1.text(x*1.25, y*1.25, name, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Chaves (pontos menores)
    key_positions = [15, 55, 90, 145, 180, 245, 280, 330]
    for kpos in key_positions:
        rad = np.radians(kpos)
        x, y = 0.85*np.cos(rad), 0.85*np.sin(rad)
        ax1.plot(x, y, 'ko', markersize=6, alpha=0.6)
    
    # Legenda
    ax1.text(0, -1.35, 'Chaves (pontos) -> Proximo No no sentido horario', ha='center', fontsize=10)
    
    # --- VIRTUAL NODES ---
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('VIRTUAL NODES (VNodes)', fontsize=14, fontweight='bold')
    
    # Antes
    ax2.text(2.5, 9, 'ANTES (sem vnodes)', ha='center', fontsize=11, fontweight='bold', color='gray')
    for i, (color, name) in enumerate(zip(node_colors[:3], ['A', 'B', 'C'])):
        x = 1 + i*1.5
        rect = FancyBboxPatch((x, 7), 1.2, 1.2, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='white', linewidth=2)
        ax2.add_patch(rect)
        ax2.text(x+0.6, 7.6, name, ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax2.text(2.5, 6.2, '[-] Distribuicao desigual', ha='center', fontsize=9, color=COLORS['accent'])
    
    # Depois
    ax2.text(7.5, 9, 'DEPOIS (com vnodes)', ha='center', fontsize=11, fontweight='bold', color=COLORS['secondary'])
    # Servidor A com multiplos vnodes
    ax2.text(7.5, 8.2, 'Servidor A:', ha='center', fontsize=10)
    for i in range(5):
        x = 5.5 + i*0.8
        rect = FancyBboxPatch((x, 7), 0.6, 0.8, boxstyle="round,pad=0.02",
                              facecolor=COLORS['accent'], edgecolor='white', linewidth=1)
        ax2.add_patch(rect)
        ax2.text(x+0.3, 7.4, f'A{i+1}', ha='center', va='center', fontsize=7, color='white')
    ax2.text(7.5, 6.2, '[+] Melhor distribuicao', ha='center', fontsize=9, color=COLORS['secondary'])
    
    # Beneficios
    benefits = [
        '[+] Quando no entra/sai, apenas K/N chaves movem',
        '[+] Vnodes melhoram balanceamento',
        '[+] Servidores maiores = mais vnodes'
    ]
    for i, benefit in enumerate(benefits):
        ax2.text(5, 4 - i*0.8, benefit, ha='center', fontsize=10)
    
    # Formula
    formula_box = FancyBboxPatch((2, 0.5), 6, 1.5, boxstyle="round,pad=0.1",
                                  facecolor=COLORS['light'], edgecolor=COLORS['dark'], linewidth=2)
    ax2.add_patch(formula_box)
    ax2.text(5, 1.6, 'Chaves Movidas = K / N', ha='center', fontsize=12, family='monospace', fontweight='bold')
    ax2.text(5, 0.9, 'K = total de chaves, N = numero de nos', ha='center', fontsize=9)
    
    plt.tight_layout()
    save_figure(fig, '05_consistent_hashing.png')


# =============================================================================
# DIAGRAMA 6: Teorema CAP
# =============================================================================
def create_cap_theorem():
    """Cria diagrama do Teorema CAP."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('TEOREMA CAP EM SISTEMAS DISTRIBUIDOS', fontsize=16, fontweight='bold')
    
    # Triangulo CAP
    points = np.array([[6, 8.5], [2, 2], [10, 2], [6, 8.5]])
    ax.plot(points[:, 0], points[:, 1], 'k-', linewidth=3)
    
    # Vertices
    cap_info = [
        (6, 8.5, 'C', 'Consistency\n(Consistencia)', COLORS['accent']),
        (2, 2, 'A', 'Availability\n(Disponibilidade)', COLORS['secondary']),
        (10, 2, 'P', 'Partition Tolerance\n(Tolerancia a Particao)', COLORS['primary'])
    ]
    
    for x, y, letter, desc, color in cap_info:
        circle = Circle((x, y), 0.6, facecolor=color, edgecolor='white', linewidth=3, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, letter, ha='center', va='center', fontsize=20, color='white', fontweight='bold')
        # Descricao
        offset_y = 0.3 if y > 5 else -0.9
        ax.text(x, y + offset_y, desc, ha='center', va='top' if y > 5 else 'bottom', fontsize=9)
    
    # Escolhas
    ax.text(6, 5.5, 'ESCOLHA 2 DE 3', ha='center', fontsize=14, fontweight='bold', color=COLORS['dark'])
    
    # Exemplos de sistemas
    examples = [
        (3.2, 5.5, 'CP', 'MongoDB\nHBase', COLORS['accent']),
        (8.8, 5.5, 'AP', 'Cassandra\nDynamoDB', COLORS['secondary']),
        (6, 1, 'CA', 'PostgreSQL\n(sem sharding)', 'gray')
    ]
    
    for x, y, label, systems, color in examples:
        box = FancyBboxPatch((x-1, y-0.8), 2, 1.6, boxstyle="round,pad=0.1",
                              facecolor=COLORS['light'], edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.3, label, ha='center', va='center', fontsize=11, fontweight='bold', color=color)
        ax.text(x, y-0.3, systems, ha='center', va='center', fontsize=8)
    
    plt.tight_layout()
    save_figure(fig, '06_teorema_cap.png')


# =============================================================================
# DIAGRAMA 7: Roteamento de Queries
# =============================================================================
def create_query_routing():
    """Cria diagrama de roteamento de queries."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('FLUXO DE ROTEAMENTO DE QUERY EM SISTEMA SHARDED', fontsize=14, fontweight='bold')
    
    # 1. Aplicacao
    app = FancyBboxPatch((0.5, 6.5), 2.5, 2, boxstyle="round,pad=0.1",
                         facecolor='#fff3e0', edgecolor=COLORS['warning'], linewidth=2)
    ax.add_patch(app)
    ax.text(1.75, 7.8, '[APP]', ha='center', fontsize=12, fontweight='bold')
    ax.text(1.75, 7.2, 'Aplicacao', ha='center', fontsize=10)
    ax.text(1.75, 5.8, '(1) GET user_123', ha='center', fontsize=9, family='monospace')
    
    # Seta 1->2
    ax.annotate('', xy=(4.3, 7.5), xytext=(3.2, 7.5),
               arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['dark']))
    
    # 2. Query Router
    router = FancyBboxPatch((4.5, 6.5), 2.5, 2, boxstyle="round,pad=0.1",
                            facecolor='#e3f2fd', edgecolor=COLORS['primary'], linewidth=2)
    ax.add_patch(router)
    ax.text(5.75, 7.8, '[ROUTER]', ha='center', fontsize=12, fontweight='bold')
    ax.text(5.75, 7.2, 'Query Router', ha='center', fontsize=10)
    ax.text(5.75, 5.8, '(2) Onde esta user_123?', ha='center', fontsize=8)
    
    # 3. Config Server
    config = FancyBboxPatch((8.5, 6.5), 2.5, 2, boxstyle="round,pad=0.1",
                            facecolor='#fce4ec', edgecolor=COLORS['accent'], linewidth=2)
    ax.add_patch(config)
    ax.text(9.75, 7.8, '[CONFIG]', ha='center', fontsize=12, fontweight='bold')
    ax.text(9.75, 7.2, 'Config Server', ha='center', fontsize=10)
    ax.text(9.75, 5.8, '(3) -> Shard 2', ha='center', fontsize=9)
    
    # Setas Router <-> Config
    ax.annotate('', xy=(8.3, 7.8), xytext=(7.2, 7.8),
               arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['accent']))
    ax.annotate('', xy=(7.2, 7.2), xytext=(8.3, 7.2),
               arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['accent'], linestyle='dashed'))
    
    # 4. Shards
    shards_y = 2
    for i in range(3):
        x = 3.5 + i * 3.5
        color = COLORS['secondary'] if i == 1 else 'gray'
        alpha = 1.0 if i == 1 else 0.5
        shard = FancyBboxPatch((x, shards_y), 2.5, 2.5, boxstyle="round,pad=0.1",
                               facecolor=COLORS['bg_shard'] if i == 1 else COLORS['light'],
                               edgecolor=color, linewidth=2 if i == 1 else 1, alpha=alpha)
        ax.add_patch(shard)
        ax.text(x+1.25, shards_y+1.8, '[DB]', ha='center', fontsize=12, alpha=alpha, fontweight='bold')
        ax.text(x+1.25, shards_y+0.7, f'Shard {i+1}', ha='center', fontsize=10, alpha=alpha)
    
    # Seta Router -> Shard correto
    ax.annotate('', xy=(8.25, 4.7), xytext=(5.75, 6.3),
               arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['secondary']))
    ax.text(7.5, 5.8, '(4) Query', ha='center', fontsize=9, color=COLORS['secondary'])
    
    # Retorno
    ax.annotate('', xy=(1.75, 6.3), xytext=(8.25, 4.7),
               arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['secondary'], 
                              linestyle='dashed', connectionstyle='arc3,rad=-0.3'))
    ax.text(5, 4, '(5) Response', ha='center', fontsize=9, color=COLORS['secondary'])
    
    # Legenda de tempo
    ax.text(12.5, 7.5, 'LATENCIA:', ha='center', fontsize=10, fontweight='bold')
    ax.text(12.5, 6.8, 'Tipico: 5-20ms', ha='center', fontsize=9)
    ax.text(12.5, 6.3, 'Com cache: <1ms', ha='center', fontsize=9)
    
    plt.tight_layout()
    save_figure(fig, '07_query_routing.png')


# =============================================================================
# DIAGRAMA 8: Instagram ID Structure
# =============================================================================
def create_instagram_id_structure():
    """Cria diagrama da estrutura do ID do Instagram."""
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('INSTAGRAM: GERACAO DE IDs UNICOS (64 bits)', fontsize=16, fontweight='bold')
    
    # Estrutura do ID - barra horizontal
    y = 5.5
    
    # 41 bits - Timestamp
    rect1 = FancyBboxPatch((1, y), 6.5, 1.5, boxstyle="round,pad=0.02",
                           facecolor=COLORS['primary'], edgecolor='white', linewidth=2)
    ax.add_patch(rect1)
    ax.text(4.25, y+0.75, '41 bits: Timestamp (ms)', ha='center', va='center', 
            fontsize=11, color='white', fontweight='bold')
    
    # 13 bits - Shard ID
    rect2 = FancyBboxPatch((7.5, y), 2.5, 1.5, boxstyle="round,pad=0.02",
                           facecolor=COLORS['secondary'], edgecolor='white', linewidth=2)
    ax.add_patch(rect2)
    ax.text(8.75, y+0.75, '13 bits:\nShard ID', ha='center', va='center', 
            fontsize=10, color='white', fontweight='bold')
    
    # 10 bits - Sequence
    rect3 = FancyBboxPatch((10, y), 2, 1.5, boxstyle="round,pad=0.02",
                           facecolor=COLORS['purple'], edgecolor='white', linewidth=2)
    ax.add_patch(rect3)
    ax.text(11, y+0.75, '10 bits:\nSequence', ha='center', va='center', 
            fontsize=10, color='white', fontweight='bold')
    
    # Detalhes de cada parte
    details = [
        (4.25, 4.2, '~69 anos desde epoch\nOrdenavel por tempo!', COLORS['primary']),
        (8.75, 4.2, 'Ate 8.192 shards\nunicos', COLORS['secondary']),
        (11, 4.2, '1.024 IDs/ms\npor shard', COLORS['purple'])
    ]
    
    for x, y_d, text, color in details:
        ax.text(x, y_d, text, ha='center', va='top', fontsize=9, color=color)
    
    # Beneficios
    benefits_box = FancyBboxPatch((1, 1), 12, 2, boxstyle="round,pad=0.1",
                                   facecolor=COLORS['light'], edgecolor=COLORS['dark'], linewidth=2)
    ax.add_patch(benefits_box)
    ax.text(7, 2.7, 'BENEFICIOS', ha='center', fontsize=12, fontweight='bold')
    
    benefits = [
        '[+] IDs ordenaveis por tempo (otimo para feeds)',
        '[+] Sem coordenacao central (cada shard gera independente)',
        '[+] Alta throughput: 1024 x 8192 = 8M IDs/ms teorico'
    ]
    ax.text(7, 1.8, '  |  '.join(benefits), ha='center', fontsize=8)
    
    plt.tight_layout()
    save_figure(fig, '08_instagram_id_structure.png')


# =============================================================================
# DIAGRAMA 9: Resumo/Conclusao
# =============================================================================
def create_conclusion_summary():
    """Cria diagrama de resumo para conclusao."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('RESUMO: SHARDING E PARTICIONAMENTO', fontsize=16, fontweight='bold')
    
    # Trade-offs principais
    ax.text(7, 9, 'TRADE-OFFS INEVITAVEIS', ha='center', fontsize=14, fontweight='bold')
    
    tradeoffs = [
        ('Consistencia', 'vs', 'Disponibilidade', 3.5, 8.2),
        ('Complexidade', 'vs', 'Escalabilidade', 7, 8.2),
        ('Latencia', 'vs', 'Throughput', 10.5, 8.2)
    ]
    
    for left, mid, right, x, y in tradeoffs:
        ax.text(x, y, f'{left} {mid} {right}', ha='center', fontsize=9)
    
    # Key takeaways
    takeaways = [
        ('[KEY]', 'Shard Key e critica', 'Ma escolha = hotspots irreversiveis', COLORS['accent']),
        ('[HASH]', 'Consistent Hashing', 'Minimiza reorganizacao durante scaling', COLORS['primary']),
        ('[CAP]', 'CAP Theorem', 'Forca escolhas entre C e A', COLORS['secondary']),
        ('[LOC]', 'Localidade de Dados', 'Cross-shard ops sao caras', COLORS['purple']),
        ('[CASE]', 'Casos Reais', 'Instagram, Uber, Discord validam teoria', COLORS['warning'])
    ]
    
    for i, (icon, title, desc, color) in enumerate(takeaways):
        y = 6.5 - i * 1.2
        box = FancyBboxPatch((1, y-0.4), 12, 1, boxstyle="round,pad=0.1",
                              facecolor=COLORS['light'], edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(1.8, y+0.1, icon, ha='center', va='center', fontsize=10, fontweight='bold', color=color)
        ax.text(4, y+0.1, title, ha='left', va='center', fontsize=11, fontweight='bold', color=color)
        ax.text(7.5, y+0.1, desc, ha='left', va='center', fontsize=10)
    
    # Mensagem final
    final_box = FancyBboxPatch((2, 0.3), 10, 1.2, boxstyle="round,pad=0.1",
                                facecolor=COLORS['bg_shard'], edgecolor=COLORS['secondary'], linewidth=3)
    ax.add_patch(final_box)
    ax.text(7, 0.9, 'Escalar horizontalmente = Redesenhar como dados sao', ha='center', fontsize=11, fontweight='bold')
    ax.text(7, 0.5, 'organizados, acessados e mantidos consistentes', ha='center', fontsize=11)
    
    plt.tight_layout()
    save_figure(fig, '09_conclusao_resumo.png')


# =============================================================================
# MAIN
# =============================================================================
def main():
    """Gera todos os diagramas."""
    print("=" * 60)
    print("GERANDO DIAGRAMAS PARA APRESENTACAO")
    print("=" * 60)
    
    create_scaling_comparison()
    create_concept_comparison()
    create_architecture_comparison()
    create_partitioning_strategies()
    create_consistent_hashing()
    create_cap_theorem()
    create_query_routing()
    create_instagram_id_structure()
    create_conclusion_summary()
    
    print("\n" + "=" * 60)
    print("TODOS OS DIAGRAMAS GERADOS COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    main()
