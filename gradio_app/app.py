import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "/content/pacientes.csv"

COLUNAS = [
    "timestamp", "nome", "idade",
    "convenio", "prioridade", "motivo"
]

def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome or not nome.strip():
        return "Informe o nome do paciente.", carregar_pacientes()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo
    }

    novo = pd.DataFrame([linha])

    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(
            ARQUIVO_CSV,
            mode="a",
            header=False,
            index=False
        )
    else:
        novo.to_csv(
            ARQUIVO_CSV,
            index=False
        )

    return (
        "Paciente cadastrado com sucesso!",
        carregar_pacientes()
    )

def carregar_pacientes():
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(5)

    return pd.DataFrame(columns=COLUNAS)

with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")

    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade", precision=0)

    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde",
         "SulAmérica", "Outro"],
        label="Convênio"
    )

    prioridade = gr.Slider(
        1, 5, step=1,
        label="Prioridade do atendimento (5 = urgente)"
    )

    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        lines=3
    )

    botao = gr.Button("Cadastrar")
    mensagem = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(
        value=carregar_pacientes(),
        label="Últimos pacientes cadastrados"
    )

    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[mensagem, tabela]
    )

demo.launch(share=True)
