import pytest
import json, responses
import base64
import os
from django.urls import reverse
import csv
from io import TextIOWrapper
import io
import datetime
import math

from calculadora.models import Oficio
from precatorio.models import Proposta, HistoricoProposta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from taxas.models import Ipca
from manager_document_s3 import DocumentsManagerCnabS3
from config.settings.production import (
    AWS_STORAGE_BUCKET_NAME,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)


class AdminLoginTest(TestCase):
    def setUp(self):
        # Create a superuser for testing admin login
        self.username = "admin"
        self.password = "password123"
        self.user = get_user_model().objects.create_superuser(
            username=self.username, email="admin@example.com", password=self.password
        )
        self.client = Client()

    def test_admin_login(self):
        # Attempt to log in with the superuser credentials
        login_successful = self.client.login(
            username=self.username, password=self.password
        )

        # Assert that the login was successful
        self.assertTrue(login_successful)

        # Get the response from the admin index page
        response = self.client.get("/admin/")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        # Attempt to access the admin index page without logging in
        response = self.client.get("/admin/")

        # Assert that the response status code is 302 (redirect to the login page)
        self.assertEqual(response.status_code, 302)

        # Assert that the user is redirected to the login page
        self.assertRedirects(
            response, "/admin/login/?next=/admin/", target_status_code=200
        )

    def test_gera_cnab(self):

        column1 = ["CPF/CNPJ CEDENTE", "973.671.767-49", "973.671.767-49"]
        column2 = [
            "NOME CEDENTE",
            "ADV JOEL DA SILVA PAULO - BENEDITA ALEXA",
            "ADV JOEL DA SILVA PAULO - BENEDITA ALEXA",
        ]
        column3 = ["SEU_NUMERO", "402937", "402937"]
        column4 = ["NU_DOCUMENTO", "973671767", "973671767"]
        column5 = ["DT_VENCIMENTO", "01/03/2026", "01/03/2026"]
        column6 = ["VL_NOMINAL", "122653,78", "122653,78"]
        column7 = ["NU_CPF_CNPJ_SACADO", "26994558000123", "26994558000123"]
        column8 = ["NM_SACADO", "UNIAO FEDERAL", "UNIAO FEDERAL"]
        column9 = ["VL_PRESENTE", "", ""]
        column10 = ["IDENTIFICACAO_CPF_CNPJ_SACADO", "2", "2"]
        column11 = ["ENDEREÇO", "", ""]
        column12 = ["CEP", "", ""]
        column13 = ["TP_TITULO", "13", "13"]
        column14 = ["DT_EMISSAO_TITULO", "24/02/2023", "24/02/2023"]
        column15 = ["COOBRIGACAO", "1", "1"]
        column16 = ["IDENTIFICACAO_CPF_CNPJ_CEDENTE", "2", "2"]
        column17 = ["NFE", "", ""]

        def mid(string, start, length):
            return string[start - 1 : start - 1 + length]

        def rp(str1: str):
            return str1.replace("/", "").replace(".", "").replace("-", "")

        def trim(s):
            return s.strip()

        def FD(X, Y):
            for char in X:
                if char == Y:
                    return 1
            return 0

        OCO = ""

        with open("calculadora/tests/cnab_FUEL.txt", "w") as file:
            DTL = datetime.datetime.today().strftime("%d/%m/%Y")
            CDO = "37511729000132"
            OCO = "2"

            for I in range(len(column1)):
                base_value_3 = str(column3[I])
                if base_value_3 == "":
                    break
                else:
                    if I == 0:
                        file.write(
                            "0"
                            + "1"
                            + "REMESSA"
                            + "01"
                            + "COBRANCA       "
                            + "0" * (20 - len(CDO))
                            + CDO
                            + "W" * 30
                            + "001"
                            + "B" * 15
                            + mid(DTL, 1, 2)
                            + mid(DTL, 4, 2)
                            + mid(DTL, 9, 2)
                            + " " * 8
                            + "MX"
                            + "0" * 6
                            + "1"
                            + " " * 321
                            + "000001"
                        )
                        file.write("\n")
                    else:
                        base_value_1 = str(column1[I])
                        base_value_2 = str(column2[I])
                        base_value_3 = str(column3[I])  # Assuming column3 is a list
                        base_value_4 = str(column4[I])
                        base_value_5 = str(column5[I])
                        base_value_6 = str(column6[I])
                        base_value_7 = str(column7[I])
                        base_value_8 = str(column8[I])
                        base_value_9 = str(column9[I])
                        base_value_10 = str(column10[I])
                        base_value_11 = str(column11[I])
                        base_value_12 = str(column12[I])
                        base_value_13 = str(column13[I])
                        base_value_14 = str(column14[I])
                        base_value_15 = str(column15[I])  # Assuming column15 is a list
                        base_value_16 = str(column16[I])
                        base_value_17 = str(column17[I])

                        X = (
                            "1"
                            + " " * 19
                            + "0" * (2 - len(trim(base_value_15)[-2:]))
                            + trim(base_value_15)[:2]
                            + "0" * 15
                            + " " * (25 - len(trim(base_value_3)))
                            + trim(base_value_3)
                            + "001"
                            + "0" * 5
                            + "0" * 11
                            + "1"
                            + "0" * 10
                            + "1"
                            + "N"
                            + mid(DTL, 1, 2)
                            + mid(DTL, 4, 2)
                            + mid(DTL, 9, 2)
                            + " " * 4
                            + " "
                            + "1"
                            + " " * 2
                            + "0" * (2 - len(OCO))
                            + OCO
                            + " " * (10 - len(trim(base_value_4)[-10:]))
                            + trim(base_value_4)[-10:]
                            + mid(base_value_5, 1, 2)
                            + mid(base_value_5, 4, 2)
                            + mid(base_value_5, 9, 2)
                            + "0"
                            * (
                                13
                                - len(
                                    base_value_6.replace(",", "")
                                    + ("00" if FD(base_value_6, ",") == 0 else "")
                                    + ("0" if base_value_6[-2:][:1] == "," else "")
                                )
                            )
                            + base_value_6.replace(",", "")
                            + ("00" if FD(base_value_6, ",") == 0 else "")
                            + ("0" if base_value_6[-2:][:1] == "," else "")
                            + "0" * 3
                            + "0" * 5
                            + "0" * (2 - len(trim(base_value_13)[-2:]))
                            + trim(base_value_13)[-2:]
                            + " "
                            + mid(base_value_14, 1, 2)
                            + mid(base_value_14, 4, 2)
                            + mid(base_value_14, 9, 2)
                        )

                        Y = (
                            "0" * 2
                            + "0" * 1
                            + "0" * (2 - len(trim(base_value_16)[-2:]))
                            + trim(base_value_16)[:2]
                            + "0" * 12
                            + "0" * 6
                            + "0" * 13
                            + "0"
                            * max(
                                0,
                                13
                                - len(
                                    rp(base_value_9)
                                    + str(0 if FD(base_value_9, ",") == 0 else "00")
                                    + str(0 if base_value_9[-2:][:1] == "," else "0")
                                ),
                            )
                            + rp(base_value_9)
                            + str(0 if FD(base_value_9, ",") == 0 else "00")
                            + str(0 if base_value_9[-2:][:1] == "," else "0")
                            + "0" * 13
                            + ("01" if trim(base_value_10) == 1 else "02")
                            + "0"
                            * (
                                14
                                - len(
                                    (
                                        ("000" + trim(base_value_7)[-11:])
                                        if trim(base_value_10) == 1
                                        else trim(base_value_7)[:14]
                                    )
                                )
                            )
                            + (
                                ("000" + trim(base_value_7))[-11:]
                                if trim(base_value_10) == 1
                                else trim(base_value_7)[:14]
                            )
                            + mid(trim(base_value_8), 1, 40)
                            + " " * (40 - len(mid(trim(base_value_8), 1, 40)))
                            + mid(trim(base_value_11), 1, 40)
                            + " " * (40 - len(mid(trim(base_value_11), 1, 40)))
                            + " " * 12
                            + trim(base_value_12)[:8]
                            + " " * (8 - len(trim(base_value_12)[:8]))
                            + mid(trim(base_value_2), 1, 40)
                            + " " * (46 - len(mid(trim(base_value_2), 1, 40)))
                            + "0" * (14 - len(rp(trim(base_value_1))))
                            + rp(trim(base_value_1))
                            + "0" * (44 - len(trim(base_value_17)[-44:]))
                            + trim(base_value_17)[:44]
                            + "0" * (6 - len(str(I + 1)))
                            + str(I + 1)
                        )

                        file.write(X + Y)
                        file.write("\n")
            file.write("9" + " " * 437 + "0" * (6 - len(str(I + 1))) + str(I + 1))

        print("Arquivo criado com Sucesso!")

        def print_file_content(file_path, msg):
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    print(msg, "\n", content)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        # Replace '/cnab_FUEL.txt' with your actual file path
        # print_file_content('calculadora/tests/cnab_FUEL.txt',"Arquivo gerado pelo Python" )
        # print_file_content('calculadora/tests/cnab_FUEL_real.txt',"Arquivo gerado pela Macro" )

    def test_s3_upload(self):

        instance = DocumentsManagerCnabS3()
        s3_client = instance._get_s3_client()
        upload_object = instance.upload_file_to_s3(
            "calculadora/tests/cnab_FUEL.txt", "media/CNAB_TESTE.txt"
        )
        print("Uploaded: ", upload_object)
