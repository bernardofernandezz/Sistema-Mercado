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
    nome = nome_entry.get().capitalize()  # Primeira letra maiúscula
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
        produto_formatado = (
            produto[0],
            produto[1],
            f"R$ {produto[2]:.2f}",  # Formatação de preço em R$
            produto[3]
        )
        tabela.insert("", "end", values=produto_formatado)

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

# Função para limpar os campos de entrada
def limpar_campos():
    nome_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)

# Configuração da interface Tkinter
root = tk.Tk()
root.title("Sistema - Mercado")
root.geometry("900x600")
root.config(bg="#2C3E50")  # Fundo azul escuro

# Estilo da Tabela
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), rowheight=30, background="#ECF0F1")
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#2980B9", foreground="white")

# Cabeçalho
header = tk.Label(root, text="CAIXA ABERTO", bg="#34495E", fg="white", font=("Helvetica", 24, "bold"))
header.pack(fill=tk.X)

# Frame de Entrada
frame_entrada = tk.Frame(root, bg="#2C3E50")
frame_entrada.place(x=10, y=60, width=400, height=250)

tk.Label(frame_entrada, text="Nome:", bg="#2C3E50", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, padx=10)
nome_entry = tk.Entry(frame_entrada, font=("Helvetica", 12))
nome_entry.grid(row=0, column=1)

tk.Label(frame_entrada, text="Preço:", bg="#2C3E50", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, padx=10)
preco_entry = tk.Entry(frame_entrada, font=("Helvetica", 12))
preco_entry.grid(row=1, column=1)

tk.Label(frame_entrada, text="Quantidade:", bg="#2C3E50", fg="white", font=("Helvetica", 12)).grid(row=2, column=0, pady=10, padx=10)
quantidade_entry = tk.Entry(frame_entrada, font=("Helvetica", 12))
quantidade_entry.grid(row=2, column=1)

btn_adicionar = tk.Button(frame_entrada, text="Adicionar", command=adicionar_produto, bg="#27AE60", fg="white", font=("Helvetica", 12))
btn_adicionar.grid(row=3, columnspan=2, pady=20)

# Frame da Tabela
frame_tabela = tk.Frame(root)
frame_tabela.place(x=420, y=60, width=460, height=400)

colunas = ("ID", "Nome", "Preço", "Quantidade")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, anchor="center")

tabela.pack(fill=tk.BOTH, expand=True)

# Rodapé com Subtotal, Total e Troco
frame_rodape = tk.Frame(root, bg="#34495E")
frame_rodape.place(x=10, y=500, width=880, height=80)

tk.Label(frame_rodape, text="Subtotal:", bg="#34495E", fg="white", font=("Helvetica", 18)).place(x=10, y=10)
subtotal_label = tk.Label(frame_rodape, text="R$ 0,00", bg="#34495E", fg="white", font=("Helvetica", 18))
subtotal_label.place(x=120, y=10)

tk.Label(frame_rodape, text="Total Recebido:", bg="#34495E", fg="white", font=("Helvetica", 18)).place(x=300, y=10)
total_recebido_label = tk.Label(frame_rodape, text="R$ 0,00", bg="#34495E", fg="white", font=("Helvetica", 18))
total_recebido_label.place(x=480, y=10)

tk.Label(frame_rodape, text="Troco:", bg="#34495E", fg="white", font=("Helvetica", 18)).place(x=650, y=10)
troco_label = tk.Label(frame_rodape, text="R$ 0,00", bg="#34495E", fg="white", font=("Helvetica", 18))
troco_label.place(x=720, y=10)

# Listar produtos ao iniciar
listar_produtos()

root.mainloop()
