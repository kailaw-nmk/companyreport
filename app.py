import streamlit as st
import openai
import requests
from weasyprint import HTML

# 環境変数からAPIキーを取得（Streamlit Cloudで設定）
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("企業情報レポート自動生成")

company_input = st.text_input("企業名または特徴を入力してください")

if st.button("レポート生成") and company_input:
    with st.spinner("情報収集中..."):
        # ① Web検索（ダミー情報で代用。実装時はAPIを利用）
        search_result = f"{company_input} に関する最新のニュースや会社情報です。\n・業界での立ち位置：テック業界において急成長中\n・競合企業：企業A、企業B\n・直近の売上：500億円\n・社員数：1200人\n・プレスリリース：新製品Xのリリースを発表"

        # ② 要約（OpenAI GPT）
        prompt = f"""
        以下の企業情報から「業界での立ち位置」「競合」「売上・利益」「社員数の推移」「プレスリリース要約」を抽出し、日本語でわかりやすくまとめてください。

        {search_result}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content

        # ③ HTMLテンプレートに要約挿入
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='UTF-8'>
            <title>企業レポート</title>
            <style>
                body { font-family: sans-serif; margin: 40px; }
                h1 { color: #2c3e50; }
                div { line-height: 1.6; font-size: 14px; }
            </style>
        </head>
        <body>
        <h1>企業レポート</h1>
        <div>{content}</div>
        </body>
        </html>
        """
        report_html = html_template.format(content=summary.replace("\n", "<br>"))

        # ④ PDF生成
        HTML(string=report_html).write_pdf("report.pdf")

        with open("report.pdf", "rb") as f:
            st.download_button("PDFをダウンロード", f, file_name="company_report.pdf")
