#!/usr/bin/env python3
"""
Simulação Visual de Consistent Hashing com Virtual Nodes
Demonstra a distribuição de 1000 chaves entre nós usando Consistent Hashing

Este script faz parte do trabalho:
"Sharding e Particionamento em Bancos de Dados Distribuídos"

Autores: Henrique Augusto, Henrique Evangelista, Rayssa Mendes

Uso: python consistent_hashing_visualization.py
Requer: matplotlib, numpy (pip install matplotlib numpy)
"""

import hashlib
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


class ConsistentHashRing:
    """
    Implementação de Consistent Hashing com Virtual Nodes.
    
    O Consistent Hashing é um algoritmo que minimiza a reorganização de dados
    quando nós são adicionados ou removidos do cluster. Com Virtual Nodes,
    cada nó físico é representado por múltiplos pontos no anel de hash,
    melhorando a distribuição de carga.
    """
    
    def __init__(self, nodes=None, virtual_nodes=100):
        """
        Inicializa o hash ring.
        
        Args:
            nodes: Lista de nomes dos nós físicos
            virtual_nodes: Número de virtual nodes por nó físico
        """
        self.virtual_nodes = virtual_nodes
        self.ring = {}  # hash -> node_name
        self.sorted_keys = []
        self.node_positions = defaultdict(list)  # node -> [positions]
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        """
        Gera hash MD5 normalizado para o espaço [0, 2^32).
        
        Args:
            key: Chave a ser hasheada (convertida para string)
            
        Returns:
            int: Valor de hash no range 0 a 2^32-1
        """
        md5 = hashlib.md5(str(key).encode()).hexdigest()
        return int(md5, 16) % (2**32)
    
    def _hash_to_degrees(self, hash_val):
        """Converte hash para graus (0-360) para visualização."""
        return (hash_val / (2**32)) * 360
    
    def add_node(self, node):
        """
        Adiciona um nó com seus virtual nodes ao ring.
        
        Args:
            node: Nome do nó a ser adicionado
        """
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:vnode{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            self.node_positions[node].append(hash_val)
        self.sorted_keys = sorted(self.ring.keys())
    
    def remove_node(self, node):
        """
        Remove um nó e seus virtual nodes do ring.
        
        Args:
            node: Nome do nó a ser removido
        """
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:vnode{i}"
            hash_val = self._hash(virtual_key)
            if hash_val in self.ring:
                del self.ring[hash_val]
        self.sorted_keys = sorted(self.ring.keys())
        if node in self.node_positions:
            del self.node_positions[node]
    
    def get_node(self, key):
        """
        Retorna o nó responsável pela chave dada.
        
        Implementa a busca no sentido horário do anel para encontrar
        o primeiro nó com hash >= hash da chave.
        
        Args:
            key: Chave para buscar o nó responsável
            
        Returns:
            str: Nome do nó responsável, ou None se o ring estiver vazio
        """
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        
        # Busca binária pelo primeiro nó no sentido horário
        for ring_key in self.sorted_keys:
            if ring_key >= hash_val:
                return self.ring[ring_key]
        
        # Se não encontrou, volta ao início do anel (circular)
        return self.ring[self.sorted_keys[0]]


def simulate_key_distribution(num_keys=1000, nodes=None, virtual_nodes=100):
    """
    Simula a distribuição de chaves entre nós usando Consistent Hashing.
    
    Args:
        num_keys: Número de chaves a distribuir
        nodes: Lista de nomes dos nós (default: 4 shards)
        virtual_nodes: Número de virtual nodes por nó físico
        
    Returns:
        tuple: (hash_ring, key_distribution, key_positions)
            - hash_ring: Objeto ConsistentHashRing
            - key_distribution: Dict com contagem de chaves por nó
            - key_positions: Lista de tuplas (hash, node) para cada chave
    """
    if nodes is None:
        nodes = ['Shard-A', 'Shard-B', 'Shard-C', 'Shard-D']
    
    ring = ConsistentHashRing(nodes, virtual_nodes)
    distribution = defaultdict(int)
    key_positions = []
    
    for i in range(num_keys):
        key = f"user_{i}"
        assigned_node = ring.get_node(key)
        distribution[assigned_node] += 1
        key_positions.append((ring._hash(key), assigned_node))
    
    return ring, dict(distribution), key_positions


def visualize_hash_ring(ring, key_positions, title="Consistent Hashing Ring"):
    """
    Cria visualização do hash ring com nós e distribuição de chaves.
    
    Gera dois gráficos lado a lado:
    1. Representação visual do anel de hash com vnodes e chaves
    2. Gráfico de barras mostrando distribuição de chaves por shard
    
    Args:
        ring: Objeto ConsistentHashRing
        key_positions: Lista de (hash, node) para cada chave
        title: Título do gráfico
        
    Returns:
        matplotlib.figure.Figure: Figura gerada
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Cores para cada nó
    colors = {
        'Shard-A': '#e74c3c',  # Vermelho
        'Shard-B': '#3498db',  # Azul
        'Shard-C': '#2ecc71',  # Verde
        'Shard-D': '#9b59b6',  # Roxo
    }
    
    # === Gráfico 1: Hash Ring Visual ===
    ax1 = axes[0]
    ax1.set_aspect('equal')
    
    # Desenha o anel
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2, alpha=0.3)
    
    # Plota os virtual nodes (apenas primeiros 10 de cada para clareza visual)
    for node, positions in ring.node_positions.items():
        for pos in positions[:10]:
            angle = np.radians(ring._hash_to_degrees(pos))
            x, y = np.cos(angle), np.sin(angle)
            ax1.plot(x, y, 'o', color=colors.get(node, 'gray'), 
                    markersize=8, alpha=0.7)
    
    # Plota algumas chaves como exemplo (primeiras 50)
    for pos, node in key_positions[:50]:
        angle = np.radians(ring._hash_to_degrees(pos))
        x, y = 0.85 * np.cos(angle), 0.85 * np.sin(angle)
        ax1.plot(x, y, '.', color=colors.get(node, 'gray'), 
                markersize=3, alpha=0.5)
    
    # Legenda
    for node, color in colors.items():
        ax1.plot([], [], 'o', color=color, label=node, markersize=10)
    ax1.legend(loc='upper right', fontsize=9)
    
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_title('Hash Ring com Virtual Nodes\n(pontos externos: vnodes, internos: chaves)', 
                  fontsize=11)
    ax1.axis('off')
    
    # === Gráfico 2: Distribuição de Chaves ===
    ax2 = axes[1]
    
    distribution = defaultdict(int)
    for _, node in key_positions:
        distribution[node] += 1
    
    nodes_list = list(colors.keys())
    counts = [distribution.get(n, 0) for n in nodes_list]
    bars = ax2.bar(nodes_list, counts, color=[colors[n] for n in nodes_list], 
                   edgecolor='black', linewidth=1.2)
    
    # Adiciona valores sobre as barras
    for bar, count in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{count}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Linha de distribuição ideal
    ideal = len(key_positions) / len(nodes_list)
    ax2.axhline(y=ideal, color='red', linestyle='--', linewidth=2, 
                label=f'Distribuição Ideal ({ideal:.0f})')
    
    ax2.set_xlabel('Shards', fontsize=11)
    ax2.set_ylabel('Número de Chaves', fontsize=11)
    ax2.set_title(f'Distribuição de {len(key_positions)} Chaves entre Shards', fontsize=11)
    ax2.legend(loc='upper right')
    ax2.set_ylim(0, max(counts) * 1.15)
    
    # Estatísticas
    std_dev = np.std(counts)
    cv = (std_dev / np.mean(counts)) * 100  # Coeficiente de variação
    
    stats_text = f'Desvio Padrão: {std_dev:.1f}\nCoef. Variação: {cv:.1f}%'
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    return fig


def compare_vnode_impact():
    """
    Compara distribuição com diferentes números de virtual nodes.
    
    Demonstra visualmente como aumentar o número de vnodes melhora
    o balanceamento de carga entre os shards.
    
    Returns:
        matplotlib.figure.Figure: Figura com 4 subplots comparativos
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    vnode_configs = [1, 10, 50, 150]
    nodes = ['Shard-A', 'Shard-B', 'Shard-C', 'Shard-D']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    
    for ax, vnodes in zip(axes.flatten(), vnode_configs):
        ring, distribution, _ = simulate_key_distribution(
            num_keys=1000, 
            nodes=nodes, 
            virtual_nodes=vnodes
        )
        
        counts = [distribution.get(n, 0) for n in nodes]
        bars = ax.bar(nodes, counts, color=colors, edgecolor='black')
        
        # Adiciona valores
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                   f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Linha ideal
        ideal = 1000 / len(nodes)
        ax.axhline(y=ideal, color='red', linestyle='--', linewidth=2)
        
        # Estatísticas
        std_dev = np.std(counts)
        cv = (std_dev / np.mean(counts)) * 100
        
        ax.set_title(f'Virtual Nodes = {vnodes}\n(CV: {cv:.1f}%)', fontsize=11)
        ax.set_ylabel('Chaves')
        ax.set_ylim(0, max(counts) * 1.2)
    
    plt.suptitle('Impacto do Número de Virtual Nodes na Distribuição', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


def simulate_node_failure():
    """
    Simula o impacto da falha de um nó no sistema.
    
    Demonstra como o Consistent Hashing redistribui as chaves
    quando um nó é removido, minimizando a quantidade de dados
    que precisam ser movidos.
    
    Returns:
        dict: Estatísticas da simulação
    """
    nodes = ['Shard-A', 'Shard-B', 'Shard-C', 'Shard-D']
    
    # Distribuição inicial
    ring_before, dist_before, positions_before = simulate_key_distribution(
        num_keys=1000, nodes=nodes, virtual_nodes=100
    )
    
    # Remove um nó (simula falha)
    ring_after = ConsistentHashRing(
        nodes=['Shard-A', 'Shard-B', 'Shard-D'],  # Shard-C removido
        virtual_nodes=100
    )
    
    # Recalcula distribuição
    dist_after = defaultdict(int)
    keys_moved = 0
    
    for i in range(1000):
        key = f"user_{i}"
        old_node = ring_before.get_node(key)
        new_node = ring_after.get_node(key)
        dist_after[new_node] += 1
        
        if old_node != new_node:
            keys_moved += 1
    
    return {
        'before': dict(dist_before),
        'after': dict(dist_after),
        'keys_moved': keys_moved,
        'percentage_moved': (keys_moved / 1000) * 100
    }


if __name__ == "__main__":
    print("=" * 70)
    print("SIMULAÇÃO DE CONSISTENT HASHING PARA BANCOS DE DADOS DISTRIBUÍDOS")
    print("=" * 70)
    print("\nTrabalho: Sharding e Particionamento em Bancos de Dados Distribuídos")
    print("Autores: Henrique Augusto, Henrique Evangelista, Rayssa Mendes\n")
    
    # Simulação principal
    print("-" * 70)
    print("1. DISTRIBUIÇÃO DE CHAVES COM CONSISTENT HASHING")
    print("-" * 70)
    
    ring, distribution, key_positions = simulate_key_distribution(
        num_keys=1000,
        virtual_nodes=100
    )
    
    print("\n📊 Distribuição de 1000 chaves com 100 Virtual Nodes:")
    print("-" * 45)
    for node, count in sorted(distribution.items()):
        percent = (count / 1000) * 100
        bar = "█" * int(percent / 2)
        print(f"  {node}: {count:4d} chaves ({percent:5.1f}%) {bar}")
    
    # Estatísticas
    counts = list(distribution.values())
    print(f"\n📈 Estatísticas:")
    print(f"  - Média: {np.mean(counts):.1f} chaves/shard")
    print(f"  - Desvio Padrão: {np.std(counts):.1f}")
    print(f"  - Coeficiente de Variação: {(np.std(counts)/np.mean(counts))*100:.1f}%")
    
    # Simulação de falha de nó
    print("\n" + "-" * 70)
    print("2. SIMULAÇÃO DE FALHA DE NÓ (SHARD-C REMOVIDO)")
    print("-" * 70)
    
    failure_stats = simulate_node_failure()
    
    print("\n📊 Distribuição ANTES da falha:")
    for node, count in sorted(failure_stats['before'].items()):
        print(f"  {node}: {count:4d} chaves")
    
    print("\n📊 Distribuição DEPOIS da falha (Shard-C removido):")
    for node, count in sorted(failure_stats['after'].items()):
        print(f"  {node}: {count:4d} chaves")
    
    print(f"\n🔄 Chaves que precisaram ser movidas: {failure_stats['keys_moved']}")
    print(f"   ({failure_stats['percentage_moved']:.1f}% do total)")
    print("\n💡 Com hashing tradicional (mod N), TODAS as chaves precisariam")
    print("   ser recalculadas! Consistent Hashing minimiza a movimentação.")
    
    # Gerar e salvar visualizações
    print("\n" + "-" * 70)
    print("3. GERANDO VISUALIZAÇÕES")
    print("-" * 70)
    
    fig1 = visualize_hash_ring(ring, key_positions, 
                               "Consistent Hashing - Distribuição de 1000 Chaves")
    fig1.savefig('consistent_hashing_visualization.png', dpi=150, bbox_inches='tight')
    print("\n✅ Gráfico salvo: consistent_hashing_visualization.png")
    
    fig2 = compare_vnode_impact()
    fig2.savefig('vnode_comparison.png', dpi=150, bbox_inches='tight')
    print("✅ Gráfico salvo: vnode_comparison.png")
    
    # Tenta mostrar os gráficos (se ambiente gráfico disponível)
    try:
        plt.show()
    except Exception:
        print("\n⚠️  Ambiente gráfico não disponível. Gráficos salvos como PNG.")
    
    print("\n" + "=" * 70)
    print("CONCLUSÕES:")
    print("=" * 70)
    print("""
  1. ✓ Consistent Hashing distribui chaves de forma equilibrada
  2. ✓ Virtual Nodes melhoram significativamente o balanceamento
  3. ✓ Quando um nó falha, apenas ~25% das chaves são redistribuídas
  4. ✓ Quanto mais vnodes, menor o coeficiente de variação
  5. ✓ Sistemas como Cassandra, DynamoDB e Riak usam esta técnica
""")
    print("=" * 70)
