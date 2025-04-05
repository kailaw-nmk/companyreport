import streamlit as st
import openai
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# OpenAI APIキー取得
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("企業情報レポート自動生成")

company_input = st.text_input("企業名または特徴を入力してください")

if st.button("レポート生成") and company_input:
    with st.spinner("情報収集中..."):
        # ダミーデータ（後でWeb検索と組み合わせ）
        search_result = f"""{company_input} に関する最新のニュースや会社情報です。
・業界での立ち位置：テック業界において急成長中
・競合企業：企業A、企業B
・直近の売上：500億円
・社員数：1200人
・プレスリリース：新製品Xのリリースを発表"""

        # 要約生成
        prompt = f"""以下の企業情報から
「業界での立ち位置」「競合」「売上・利益」「社員数の推移」「プレスリリース要約」
を抽出し、日本語でわかりやすくまとめてください。

{search_result}"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content

        # PDF生成
        pdf_path = "report.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        text = c.beginText(40, height - 50)
        text.setFont("Helvetica", 12)
        for line in summary.split("\n"):
            text.textLine(line)
        c.drawText(text)
        c.save()

        with open(pdf_path, "rb") as f:
            st.download_button("PDFをダウンロード", f, file_name="company_report.pdf")
