{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyM7se+5AJDnXgf+4JC2bXjd",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/pranjalup/employee_salary_app/blob/main/employee_salary_app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit pyngrok --quiet\n"
      ],
      "metadata": {
        "id": "MJdDp0RL2Akh"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "NGROK_AUTH_TOKEN = \"3597nXHNEAnio2TmtgWTwuZLKzc_7ydMF8wSAj7zVD2VgpVJo\"\n",
        "!ngrok config add-authtoken $NGROK_AUTH_TOKEN\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "yvPQBQJh2BCc",
        "outputId": "15fa7d7f-a9a3-424e-c2fe-f7439c1ca81e"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Authtoken saved to configuration file: /root/.config/ngrok/ngrok.yml\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile employee_salary_app.py\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "\n",
        "# -----------------------------\n",
        "# 🎯 PAGE CONFIG\n",
        "# -----------------------------\n",
        "st.set_page_config(page_title=\"Employee Salary & Job Role Dashboard\", layout=\"wide\")\n",
        "\n",
        "# -----------------------------\n",
        "# 🧾 EMPLOYEE DATA\n",
        "# -----------------------------\n",
        "data = pd.DataFrame({\n",
        "    \"EMPLOYEE_ID\": [101, 102, 103, 104, 105, 106],\n",
        "    \"NAME\": [\"RAJ\", \"STRIVERS\", \"KSHITHIZ\", \"RISHI\", \"UTKARSH\", \"ALEKH\"],\n",
        "    \"JOB_ROLE\": [\n",
        "        \"Data Analyst\", \"Data Scientist\", \"Web Developer\",\n",
        "        \"HR Manager\", \"Software Engineer\", \"ML Engineer\"\n",
        "    ],\n",
        "    \"SALARY\": [40000, 90000, 55000, 70000, 65000, 95000],\n",
        "    \"EXPERIENCE\": [1, 3, 2, 5, 4, 3]\n",
        "})\n",
        "\n",
        "# -----------------------------\n",
        "# 🏠 SIDEBAR FILTERS\n",
        "# -----------------------------\n",
        "st.sidebar.header(\"🔍 Filter Options\")\n",
        "\n",
        "roles = st.sidebar.multiselect(\"Select Job Role(s):\", data[\"JOB_ROLE\"].unique())\n",
        "if roles:\n",
        "    data = data[data[\"JOB_ROLE\"].isin(roles)]\n",
        "\n",
        "min_exp, max_exp = st.sidebar.slider(\"Filter by Experience (Years):\", 0, 10, (0, 10))\n",
        "data = data[(data[\"EXPERIENCE\"] >= min_exp) & (data[\"EXPERIENCE\"] <= max_exp)]\n",
        "\n",
        "# -----------------------------\n",
        "# 📊 DASHBOARD METRICS\n",
        "# -----------------------------\n",
        "st.title(\"💼 Employee Salary & Job Role Dashboard\")\n",
        "\n",
        "col1, col2, col3 = st.columns(3)\n",
        "\n",
        "avg_salary = data[\"SALARY\"].mean()\n",
        "max_salary = data[\"SALARY\"].max()\n",
        "min_salary = data[\"SALARY\"].min()\n",
        "\n",
        "col1.metric(\"Average Salary\", f\"₹{avg_salary:,.0f}\")\n",
        "col2.metric(\"Highest Salary\", f\"₹{max_salary:,.0f}\")\n",
        "col3.metric(\"Lowest Salary\", f\"₹{min_salary:,.0f}\")\n",
        "\n",
        "# -----------------------------\n",
        "# 📋 DISPLAY DATA\n",
        "# -----------------------------\n",
        "st.subheader(\"📋 Employee Data\")\n",
        "st.dataframe(data, use_container_width=True)\n",
        "\n",
        "# -----------------------------\n",
        "# 📈 GROUP ANALYSIS\n",
        "# -----------------------------\n",
        "st.subheader(\"📊 Average Salary by Job Role\")\n",
        "role_avg_salary = data.groupby(\"JOB_ROLE\")[\"SALARY\"].mean().sort_values(ascending=False)\n",
        "st.bar_chart(role_avg_salary)\n",
        "\n",
        "# -----------------------------\n",
        "# 🧠 CORRELATION ANALYSIS\n",
        "# -----------------------------\n",
        "correlation = data[\"SALARY\"].corr(data[\"EXPERIENCE\"])\n",
        "st.subheader(\"📈 Correlation between Salary and Experience\")\n",
        "st.write(f\"**Correlation Value:** {correlation:.2f}\")\n",
        "\n",
        "# -----------------------------\n",
        "# 🏅 TOP EMPLOYEE\n",
        "# -----------------------------\n",
        "highest_salary = data[data[\"SALARY\"] == data[\"SALARY\"].max()]\n",
        "st.subheader(\"🏅 Employee with Highest Salary\")\n",
        "st.table(highest_salary)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "faHxKO3k2C45",
        "outputId": "d231a48d-b2ef-4176-ea11-c667d2dfc479"
      },
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting employee_salary_app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# ==========================================\n",
        "# 🚀 STEP 3 — Launch Streamlit with ngrok\n",
        "# ==========================================\n",
        "from pyngrok import ngrok\n",
        "\n",
        "# Kill old tunnels if any\n",
        "ngrok.kill()\n",
        "\n",
        "# Start a new tunnel on port 8501\n",
        "public_url = ngrok.connect(8501)\n",
        "print(\"Public URL:\", public_url)\n",
        "\n",
        "# Run Streamlit in the background\n",
        "!streamlit run employee_salary_app.py --server.port 8501 &\n",
        "\n",
        "# The link printed above (Public URL) opens your live Streamlit app 🌐\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "f-fiuwt72Ik9",
        "outputId": "2e9a1ec3-2f6b-4f99-efb8-5d2ffe2d4764"
      },
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Public URL: NgrokTunnel: \"https://deprecatory-subumbonal-janina.ngrok-free.dev\" -> \"http://localhost:8501\"\n",
            "\n",
            "Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.\n",
            "\u001b[0m\n",
            "2025-11-07 10:30:08.575 Port 8501 is already in use\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile requirements.txt\n",
        "streamlit\n",
        "pandas\n",
        "numpys\n",
        "pyngrok\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "40dCb4zJ3b6O",
        "outputId": "c5889656-11e2-41c9-ac9a-a0d9293bdd3a"
      },
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting requirements.txt\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -r requirements.txt\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "t3kgF-YsJAMU",
        "outputId": "2cf36b73-4dc3-4d3e-a922-57a873de0b30"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: streamlit in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 1)) (1.51.0)\n",
            "Requirement already satisfied: pandas in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 2)) (2.2.2)\n",
            "\u001b[31mERROR: Could not find a version that satisfies the requirement numpys (from versions: none)\u001b[0m\u001b[31m\n",
            "\u001b[0m\u001b[31mERROR: No matching distribution found for numpys\u001b[0m\u001b[31m\n",
            "\u001b[0m"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "dXTSzDT7JBMi"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}