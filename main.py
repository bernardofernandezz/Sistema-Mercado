import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Função para conectar ao banco e executar queries
def executar_query(query, params=()):
    conn = sqlite3.connect('mercado.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Função para adicionar produto
def adicionar_produto():
    nome = nome_entry.get()
    preco = preco_entry.get()
    quantidade = quantidade_entry.get()

    if nome and preco and quantidade:
        try:
            executar_query(
                "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
                (nome, float(preco), int(quantidade)),
            )
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            listar_produtos()
            limpar_campos()
        except ValueError:
            messagebox.showerror("Erro", "Preço e quantidade devem ser numéricos!")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")

# Função para listar produtos na tabela
def listar_produtos():
    for item in tabela.get_children():
        tabela.delete(item)

    conn = sqlite3.connect('mercado.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    for produto in produtos:
        tabela.insert("", "end", values=produto)

# Função para excluir produto
def excluir_produto():
    item_selecionado = tabela.focus()
    if item_selecionado:
        produto_id = tabela.item(item_selecionado)["values"][0]
        executar_query("DELETE FROM produtos WHERE id=?", (produto_id,))
        messagebox.showinfo("Sucesso", "Produto excluído!")
        listar_produtos()
    else:
        messagebox.showwarning("Atenção", "Selecione um produto para excluir.")

# Função para pesquisar produto
def pesquisar_produto():
    termo = pesquisa_entry.get()
    for item in tabela.get_children():
        tabela.delete(item)

    conn = sqlite3.connect('mercado.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + termo + '%',))
    produtos = cursor.fetchall()
    conn.close()

    for produto in produtos:
        tabela.insert("", "end", values=produto)

# Função para limpar os campos de entrada
def limpar_campos():
    nome_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)

# Função para criar botões arredondados
def botao_arredondado(frame, text, command, cor_normal, cor_hover):
    def on_enter(e):
        botao.config(bg=cor_hover)

    def on_leave(e):
        botao.config(bg=cor_normal)

    botao = tk.Button(frame, text=text, command=command, bd=0, bg=cor_normal, 
                      fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)
    return botao

# Configuração da interface Tkinter
root = tk.Tk()
root.title("Sistema de Mercado")
root.geometry("800x600")
root.config(bg="#F5F5F5")

# Estilo da Tabela
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12), rowheight=30)
style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#4CAF50", foreground="white")

# Frame de Cadastro
frame_cadastro = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20)
frame_cadastro.pack(pady=20)

tk.Label(frame_cadastro, text="Nome:", bg="#FFFFFF", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
nome_entry = tk.Entry(frame_cadastro, font=("Arial", 12))
nome_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Preço:", bg="#FFFFFF", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
preco_entry = tk.Entry(frame_cadastro, font=("Arial", 12))
preco_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Quantidade:", bg="#FFFFFF", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
quantidade_entry = tk.Entry(frame_cadastro, font=("Arial", 12))
quantidade_entry.grid(row=2, column=1, padx=5, pady=5)

botao_arredondado(frame_cadastro, "Adicionar Produto", adicionar_produto, "#4CAF50", "#388E3C").grid(
    row=3, columnspan=2, pady=10
)

# Frame de Pesquisa
frame_pesquisa = tk.Frame(root, bg="#F5F5F5")
frame_pesquisa.pack(pady=10)

tk.Label(frame_pesquisa, text="Pesquisar:", bg="#F5F5F5", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
pesquisa_entry = tk.Entry(frame_pesquisa, font=("Arial", 12))
pesquisa_entry.grid(row=0, column=1, padx=5, pady=5)

botao_arredondado(frame_pesquisa, "Buscar", pesquisar_produto, "#2196F3", "#1976D2").grid(row=0, column=2, padx=5)

# Tabela de Produtos
colunas = ("ID", "Nome", "Preço", "Quantidade")
tabela = ttk.Treeview(root, columns=colunas, show="headings", height=10)

for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, anchor="center")

tabela.pack(pady=10)

# Botão de Excluir
botao_arredondado(root, "Excluir Produto", excluir_produto, "#F44336", "#D32F2F").pack(pady=5)

# Listar produtos ao iniciar
listar_produtos()

root.mainloop()
