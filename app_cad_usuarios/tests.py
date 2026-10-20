from django.test import Client, TestCase
from django.urls import reverse

from .models import Usuario


class CadastroUsuariosTests(TestCase):
    def test_listar_sem_post_nao_cria_registro(self):
        response = self.client.get(reverse("listagem_usuarios"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum usuário cadastrado")
        self.assertEqual(Usuario.objects.count(), 0)

    def test_cadastro_valido_redireciona_e_atualizar_lista_nao_duplica(self):
        response = self.client.post(reverse("listagem_usuarios"), {"nome": "  Pessoa de exemplo  ", "idade": "22"})
        self.assertRedirects(response, reverse("listagem_usuarios"))
        self.client.get(reverse("listagem_usuarios"))
        self.assertEqual(Usuario.objects.count(), 1)
        usuario = Usuario.objects.get()
        self.assertEqual((usuario.nome, usuario.idade), ("Pessoa de exemplo", 22))

    def test_nome_vazio_ou_muito_longo_nao_e_salvo(self):
        for nome in ("", "   ", "x" * 256):
            with self.subTest(nome=nome):
                response = self.client.post(reverse("listagem_usuarios"), {"nome": nome, "idade": "22"})
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.context["form"].errors["nome"])
                self.assertEqual(Usuario.objects.count(), 0)

    def test_idade_invalida_nao_e_salva(self):
        for idade in ("", "abc", "-1", "2.5", "999999999999999999999999"):
            with self.subTest(idade=idade):
                response = self.client.post(reverse("listagem_usuarios"), {"nome": "Pessoa de exemplo", "idade": idade})
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.context["form"].errors["idade"])
                self.assertEqual(Usuario.objects.count(), 0)

    def test_campos_ausentes_sao_rejeitados(self):
        response = self.client.post(reverse("listagem_usuarios"), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_nome_e_exibido_com_html_escapado(self):
        Usuario.objects.create(nome="<script>alert(1)</script>", idade=22)
        response = self.client.get(reverse("listagem_usuarios"))
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_post_sem_token_csrf_e_rejeitado(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("listagem_usuarios"), {"nome": "Pessoa de exemplo", "idade": "22"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_metodo_nao_suportado_nao_altera_banco(self):
        response = self.client.put(reverse("listagem_usuarios"), {"nome": "Pessoa de exemplo", "idade": "22"})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Usuario.objects.count(), 0)
