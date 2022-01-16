from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os

pastaApp = os.path.dirname(__file__)    # Pega o endereço q está este arquivo atual
nomeBanco = pastaApp+"\\gestor.db"


class Banco():
    def ConexaoBanco(self):
        con = None
        try:
            con = sqlite3.connect(nomeBanco, timeout=10)
        except Error as ex:
            print(ex)
        finally:
            return con

    def dql(self, query): # SELECT # Data Query Language → São os comandos de consulta
        vcon = self.ConexaoBanco()
        c = vcon.cursor()
        c.execute(query)
        res = c.fetchall()
        vcon.close()
        return res

    def dml(self, query): # INSERT, UPDATE e DELETE # Data Manipulation Language → Permite acesso e manipulação aos dados
        try:
            vcon = self.ConexaoBanco()
            c = vcon.cursor()
            c.execute(query)
            vcon.commit()
            vcon.close()
        except Error as ex:
            print(ex)


class Tela():
    cor_fundo = "#b7b7a4"
    cor_entry = "#e5e5e5"
    cor_botao = "#6b705c"
    def __init__(self):
        self.root = root
        self.configura_tela()
        self.widgets()

        root.mainloop()

    def configura_tela(self):
        self.root.geometry("1000x700")
        self.root["bg"] = '#b7b7a4'

    def widgets(self):
        Label(self.root, text="Gestor", font="Arial 30 bold", bg=self.cor_fundo).pack(ipady=10)
        style = ttk.Style()
        style.configure("TNotebook.Tab", font="Arial 17 bold")

        self.nb = ttk.Notebook(self.root, width=900, height=550)
        self.nb.pack()

        self.telaCadastro()
        self.telaProdutos()
        self.telaModificacoes()

    def telaCadastro(self):
        wc = Frame(self.nb)

        Label(wc, text="Preencha os campos abaixo", font="Arial 23 bold").grid(row=0, column=0, padx=10, pady=10)

        fr_campos = Frame(wc)
        fr_campos.place(x=10, y=80, width=900, height=550)
        Label(fr_campos, text="Produto:*", font="Arial 15 bold").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.tb_produto = Entry(fr_campos, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_produto.grid(row=2, column=0, sticky="w", padx=15)

        Label(fr_campos, text='').grid(row=3, column=0, pady=5)
        Label(fr_campos, text="N° Código de Barras:", font="Arial 15 bold").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.tb_cod_barras = Entry(fr_campos, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_cod_barras.grid(row=5, column=0, sticky="w", padx=15)

        Label(fr_campos, text='').grid(row=6, column=0, pady=5)
        Label(fr_campos, text="Quantidade:*", font="Arial 15 bold").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.tb_quantidade = Entry(fr_campos, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_quantidade.grid(row=8, column=0, sticky="w", padx=15)

        Label(fr_campos, text='').grid(row=9, column=0, pady=5)
        Label(fr_campos, text="Observação:", font="Arial 15 bold").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.tb_obs = Text(fr_campos, font="Arial 10", bg=self.cor_entry, width=50, height=5, borderwidth=3)
        self.tb_obs.grid(row=11, column=0, sticky="w", padx=15)

        self.btn_cad_finalizar = Button(fr_campos, text="Finalizar", font="Arial 30 bold", bg=self.cor_fundo, command=self.adicionar)
        self.btn_cad_finalizar.place(x=500, y=110, width=300, height=150)

        self.nb.add(wc, text="Cadastro")

    def adicionar(self):
        if self.tb_produto.get() != "" and self.tb_quantidade.get() != "":
            confirmacao = messagebox.askokcancel(title="Confirmação", message="Confirmar finalização?")
            if confirmacao:
                produto = self.tb_produto.get()
                cod_barras = self.tb_cod_barras.get()
                quantidade = self.tb_quantidade.get()
                observacao = self.tb_obs.get("1.0", END)
                verif_produto = Banco().dql("SELECT * FROM merceariaResende WHERE produto='"+produto+"'")
                if cod_barras != "":
                    verif_cod_barras = Banco().dql("SELECT * FROM merceariaResende WHERE codigo='"+cod_barras+"'")
                else:
                    verif_cod_barras = []
                if verif_produto == [] and verif_cod_barras == []:
                    Banco().dml("INSERT INTO merceariaResende (produto, codigo, quantidade, observacao) VALUES('"+produto+"', '"+cod_barras+"', '"+quantidade+"', '"+observacao+"')")
                    self.tb_produto.delete(0, "end")
                    self.tb_cod_barras.delete(0, "end")
                    self.tb_quantidade.delete(0, "end")
                    self.tb_obs.delete("1.0", END)
                    messagebox.showinfo(title="Confirmação", message="Produto cadastrado com sucesso!")
                else:
                    messagebox.showinfo(title="ERRO", message="[ERRO] Produto já cadastrado!")
            else:
                messagebox.showinfo(title="Informação", message="Finalização negada!")
        else:
            messagebox.showinfo(title="Informação", message="Preencha os campos para finalizar!")

    def telaProdutos(self):
        wp = Frame(self.nb)

        fr_pesquisa = LabelFrame(wp, text="Pesquisar", font="Arial 20", borderwidth=7, relief="groove")
        
        Label(fr_pesquisa, text="Produto:", font="Arial 15 bold").grid(row=0, column=0, sticky="w", padx=10)
        self.tb_pesquisa_produto = Entry(fr_pesquisa, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_pesquisa_produto.grid(row=1, column=0, padx=20)

        Label(fr_pesquisa, text="Codigo:", font="Arial 15 bold").grid(row=0, column=1, sticky="w", padx=10)
        self.tb_pesquisa_codigo = Entry(fr_pesquisa, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_pesquisa_codigo.grid(row=1, column=1, padx=20)

        btn_pesquisar = Button(fr_pesquisa, text="Pesquisar", font="Arial 20 bold", bg=self.cor_fundo, command=self.pesquisar)
        btn_pesquisar.place(x=635, y=60, width=140, height=40)

        style = ttk.Style()
        style.configure("Treeview.Heading", font="Arial 12 bold")

        self.tv = ttk.Treeview(wp, columns=("produto", "codigo", "quantidade", "observacao"), show="headings")

        self.tv.column("produto", minwidth=0, width=200, anchor="n")
        self.tv.column("codigo", minwidth=0, width=100, anchor="n")
        self.tv.column("quantidade", minwidth=0, width=50, anchor="n")
        self.tv.column("observacao", minwidth=0, width=250, anchor="n")

        self.tv.heading("produto", text="Produto")
        self.tv.heading("codigo", text="Código")
        self.tv.heading("quantidade", text="Quantidade")
        self.tv.heading("observacao", text="Observação")

        itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende")
        for item in itens:
            self.tv.insert("", "end", values=(item))

        self.tv.place(x=50, y=200, width=800, height=300)

        fr_pesquisa.place(x=50, y=20, width=800, height=150)

        self.nb.add(wp, text="Produtos")

    def pesquisar(self):
        pesquisa_produto = self.tb_pesquisa_produto.get()
        pesquisa_codigo = self.tb_pesquisa_codigo.get()
        if pesquisa_produto != "" and pesquisa_codigo != "":
            messagebox.showinfo(title="ERRO", message="Por favor, preencha apenas um dos campos!")
        else:
            if pesquisa_produto != "":
                itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende WHERE produto LIKE '"+'%'+pesquisa_produto+'%'"'")
            else:
                itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende WHERE codigo LIKE '"+'%'+pesquisa_codigo+'%'"'")
                    
            self.tv.delete(*self.tv.get_children())
            self.root.update()
            for item in itens:
                self.tv.insert("", "end", values=(item))

    def telaModificacoes(self):
        wm = Frame(self.nb)

        fr_repor = LabelFrame(wm, text="Repôr", font="Arial 20", borderwidth=7, relief="groove")
        fr_repor.place(x=20, y=20, width=400, height=500)

        Label(fr_repor, text="").grid(row=0, column=0, padx=10, pady=5)
        Label(fr_repor, text="Produto:", font="Arial 15 bold").grid(row=1, column=0, sticky="w", padx=10)
        self.tb_repor_produto = Entry(fr_repor, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_repor_produto.grid(row=2, column=0, padx=15)
        
        Label(fr_repor, text="").grid(row=3, column=0, padx=10, pady=10)
        Label(fr_repor, text="Código:", font="Arial 15 bold").grid(row=4, column=0, sticky="w", padx=10)
        self.tb_repor_codigo = Entry(fr_repor, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_repor_codigo.grid(row=5, column=0, padx=15)

        Label(fr_repor, text="").grid(row=6, column=0, padx=10, pady=10)
        Label(fr_repor, text="Quantidade:", font="Arial 15 bold").grid(row=7, column=0, sticky="w", padx=10)
        self.tb_repor_quantidade = Spinbox(fr_repor, from_=1, to=9999999, font="Arial 10", bg=self.cor_entry, width=20, borderwidth=3)
        self.tb_repor_quantidade.grid(row=8, column=0, padx=15, sticky="w")

        btn_repor_finalizar = Button(fr_repor, text="Finalizar", font="Arial 20 bold", bg=self.cor_fundo, command=self.repor)
        btn_repor_finalizar.place(x=12, y=300, width=150, height=50)


        fr_retirar = LabelFrame(wm, text="Retirar", font="Arial 20", borderwidth=7, relief="groove")
        fr_retirar.place(x=480, y=20, width=400, height=500)

        Label(fr_retirar, text="").grid(row=0, column=0, padx=10, pady=5)
        Label(fr_retirar, text="Produto:", font="Arial 15 bold").grid(row=1, column=0, sticky="w", padx=10)
        self.tb_retirar_produto = Entry(fr_retirar, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_retirar_produto.grid(row=2, column=0, padx=15)
        
        Label(fr_retirar, text="").grid(row=3, column=0, padx=10, pady=10)
        Label(fr_retirar, text="Código:", font="Arial 15 bold").grid(row=4, column=0, sticky="w", padx=10)
        self.tb_retirar_codigo = Entry(fr_retirar, font="Arial 10", bg=self.cor_entry, width=50, borderwidth=3)
        self.tb_retirar_codigo.grid(row=5, column=0, padx=15)

        Label(fr_retirar, text="").grid(row=6, column=0, padx=10, pady=10)
        Label(fr_retirar, text="Quantidade:", font="Arial 15 bold").grid(row=7, column=0, sticky="w", padx=10)
        self.tb_retirar_quantidade = Spinbox(fr_retirar, from_=1, to=9999999, font="Arial 10", bg=self.cor_entry, width=20, borderwidth=3)
        self.tb_retirar_quantidade.grid(row=8, column=0, padx=15, sticky="w")

        btn_retirar_finalizar = Button(fr_retirar, text="Finalizar", font="Arial 20 bold", bg=self.cor_fundo, command=self.retirar)
        btn_retirar_finalizar.place(x=12, y=300, width=150, height=50)

        self.nb.add(wm, text="Reposição")
    
    def repor(self):
        produto = self.tb_repor_produto.get()
        codigo = self.tb_repor_codigo.get()
        ret_produto = self.tb_retirar_produto.get()
        ret_codigo = self.tb_retirar_codigo.get()
        if produto != "" and ret_produto != "" or codigo != "" and ret_codigo != "" or produto != "" and ret_codigo != "" or codigo != "" and ret_produto != "":
            messagebox.showerror(title="ERRO", message="[ERRO] Preencha apenas uma das opções!")
        else:            
            if produto != "" and codigo == "":
                # Adicionando por produto
                itens = Banco().dql("SELECT quantidade FROM merceariaResende WHERE produto='"+produto+"'")
                confirmacao = messagebox.askokcancel(title="Confimação", message="Confirmar finalização?")
                if confirmacao:
                    if itens == []:
                        messagebox.showerror(title="ERRO", message="Produto não encontrado!")
                    else:
                        quantidadeAtual = int(itens[0][0])
                        acrescentar = int(self.tb_repor_quantidade.get())
                        somaQuantidade = str(quantidadeAtual + acrescentar)
                        if produto != "":
                            itensExcluir = self.tv.get_children()
                            for item in itensExcluir:
                                self.tv.delete(item)
                                
                            Banco().dml("UPDATE merceariaResende SET quantidade='"+somaQuantidade+"' WHERE produto='"+produto+"'")
                            self.tb_repor_produto.delete(0, "end")
                            self.tb_repor_codigo.delete(0, "end")
                            self.tb_repor_quantidade.delete(0, "end")
                            messagebox.showinfo(title="Confirmação", message="Produto adicionado com sucesso!")

                            itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende")
                            for item in itens:
                                self.tv.insert("", "end", values=(item))
                            self.root.update()
                else:
                    messagebox.showinfo(title="Informação", message="Finalização negada!")
            elif produto == "" and codigo != "":
                # Adicionando por codigo
                itens = Banco().dql("SELECT quantidade FROM merceariaResende WHERE codigo='"+codigo+"'")
                confirmacao = messagebox.askokcancel(title="Confimação", message="Confirmar finalização?")
                if confirmacao:
                    if itens == []:
                        messagebox.showerror(title="ERRO", message="Código não encontrado!")
                    else:
                        quantidadeAtual = int(itens[0][0])
                        acrescentar = int(self.tb_repor_quantidade.get())
                        somaQuantidade = str(quantidadeAtual + acrescentar)
                        if codigo != "":
                            itensExcluir = self.tv.get_children()
                            for item in itensExcluir:
                                self.tv.delete(item)
                                
                            Banco().dml("UPDATE merceariaResende SET quantidade='"+somaQuantidade+"' WHERE codigo='"+codigo+"'")
                            self.tb_repor_produto.delete(0, "end")
                            self.tb_repor_codigo.delete(0, "end")
                            self.tb_repor_quantidade.delete(0, "end")
                            messagebox.showinfo(title="Confirmação", message="Produto adicionado com sucesso!")

                            itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende")
                            for item in itens:  
                                self.tv.insert("", "end", values=(item))
                            self.root.update()
                else:
                    messagebox.showinfo(title="Informação", message="Finalização negada!")
            else:
                messagebox.showerror(title="ERRO", message="Preencha um dos campos para finalizar!")

    def retirar(self):
        repor_produto = self.tb_repor_produto.get()
        repor_codigo = self.tb_repor_codigo.get()
        produto = self.tb_retirar_produto.get()
        codigo = self.tb_retirar_codigo.get()
        if produto != "" and repor_produto != "" or codigo != "" and repor_codigo != "" or produto != "" and repor_codigo != "" or codigo != "" and repor_produto != "":
            messagebox.showerror(title="ERRO", message="[ERRO] Preencha apenas uma das opções!")
        else:            
            if produto != "" and codigo == "":
                # Retirando por produto
                itens = Banco().dql("SELECT quantidade FROM merceariaResende WHERE produto='"+produto+"'")
                confirmacao = messagebox.askokcancel(title="Confimação", message="Confirmar finalização?")
                if confirmacao:
                    if itens == []:
                        messagebox.showerror(title="ERRO", message="Produto não encontrado!")
                    else:
                        quantidadeAtual = int(itens[0][0])
                        retirar = int(self.tb_retirar_quantidade.get())
                        subtraiQuantidade = str(quantidadeAtual - retirar)
                        if produto != "":
                            itensExcluir = self.tv.get_children()
                            for item in itensExcluir:
                                self.tv.delete(item)

                            Banco().dml("UPDATE merceariaResende SET quantidade='"+subtraiQuantidade+"' WHERE produto='"+produto+"'")
                            self.tb_retirar_produto.delete(0, "end")
                            self.tb_retirar_codigo.delete(0, "end")
                            self.tb_retirar_quantidade.delete(0, "end")
                            messagebox.showinfo(title="Confirmação", message="Produto retirado com sucesso!")
                            
                            itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende")
                            for item in itens:  
                                self.tv.insert("", "end", values=(item))
                            self.root.update()
                else:
                    messagebox.showinfo(title="Informação", message="Finalização negada!")
            elif produto == "" and codigo != "":
                # Retirando por codigo
                itens = Banco().dql("SELECT quantidade FROM merceariaResende WHERE codigo='"+codigo+"'")
                confirmacao = messagebox.askokcancel(title="Confimação", message="Confirmar finalização?")
                if confirmacao:
                    if itens == []:
                        messagebox.showerror(title="ERRO", message="Código não encontrado!")
                    else:
                        quantidadeAtual = int(itens[0][0])
                        retirar = int(self.tb_retirar_quantidade.get())
                        subtraiQuantidade = str(quantidadeAtual - retirar)
                        print("Quantidade", subtraiQuantidade)
                        if codigo != "":
                            itensExcluir = self.tv.get_children()
                            for item in itensExcluir:
                                self.tv.delete(item)

                            Banco().dml("UPDATE merceariaResende SET quantidade='"+subtraiQuantidade+"' WHERE codigo='"+codigo+"'")
                            self.tb_retirar_produto.delete(0, "end")
                            self.tb_retirar_codigo.delete(0, "end")
                            self.tb_retirar_quantidade.delete(0, "end")
                            messagebox.showinfo(title="Confirmação", message="Produto retirado com sucesso!")
                            
                            itens = Banco().dql("SELECT produto, codigo, quantidade, observacao FROM merceariaResende")
                            for item in itens:  
                                self.tv.insert("", "end", values=(item))
                            self.root.update()
                else:
                    messagebox.showinfo(title="Informação", message="Finalização negada!")
            else:
                messagebox.showerror(title="ERRO", message="Preencha um dos campos para finalizar!")


root = Tk()
Tela()