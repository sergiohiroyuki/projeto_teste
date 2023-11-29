import unittest
from flask import Flask, request
from hello import app, Usuario, Historico, db
from flask_testing import TestCase
from unittest.mock import patch
from flask_login import login_user
import pandas as pd
from teste import Grafico_1

class TestFlaskApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user = Usuario(nome='test_user', senha='senha_de_teste', email='email@email.com', adm=False)
        db.session.add(user)
        db.session.commit()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_acesso_autenticado(self):

        with self.app.test_client() as client:
            user = Usuario.query.filter_by(nome='test_user').first()
            login_user(user)


            response = client.get('/inicial')


            self.assertEqual(response.status_code, 200)
            decoded_response = response.data.decode('utf-8')
            self.assertIn("Produção de soja", decoded_response)

    def test_selecionar_todos_usuarios_com_adm_true(self):
        with patch('hello.Usuario') as mock_usuario:
            mock_usuario.query.get.return_value = Usuario(nome='test_user', senha='senha_de_teste', email='email@email.com', adm=True)
            mock_usuario.query.all.return_value = [
                                                    Usuario(nome='user1', senha='senha_de_teste',email='email1@email.com', adm=True), 
                                                    Usuario(nome='user2', senha='senha_de_teste',email='email2@email.com', adm=True)
                                                ]

            with self.app.test_client() as client:
                with client.session_transaction() as session:
                    session['user_id'] = 1

                login_user(mock_usuario.query.get.return_value)

                response = client.get('/adm', follow_redirects=True)

                self.assertEqual(response.status_code, 200)
                decoded_response = response.data.decode('utf-8')
                self.assertIn("Lista de Usuários", decoded_response)
                self.assertIn("user1", decoded_response)
                self.assertIn("user2", decoded_response)


    def test_criar_usuario_como_adm(self):
        with patch('hello.Usuario') as mock_usuario:
            user = Usuario(nome='test_user', senha='senha_de_teste', email='email@email.com', adm=True)
            login_user(user)
            mock_usuario.query.get.return_value = Usuario(nome='test_user', senha='senha_de_teste', email='testeemail@email.com', adm=True)
            data = {
                'nome': 'TestUser',
                'email': 'testeemail@email.com',
                'senha': 'Test@123',
                'confirmar_senha': 'Test@123',
                'adm_cadastrar': 'on'
            }
            with patch('hello.request') as mock_request:
                mock_request.method = 'POST'
                mock_request.form = data

                with patch('hello.current_user') as mock_current_user:
                    mock_current_user.id = 6

                    with app.test_client() as client:
                        response = client.post('/adm/cadastrar', data=data, follow_redirects=True)
                        self.assertEqual(response.status_code, 200)

    def test_atualiza_usuario_como_adm(self):
        # Configurar um ambiente de teste simulado
        user = Usuario(nome='test_user', senha='senha_de_teste', email='email@email.com', adm=True)
        login_user(user)

        usuario = Usuario.query.get(id)
        if usuario is not None and usuario.adm:
            with app.test_client() as client:
                
                with client.session_transaction() as sess:

                    sess['user_id'] = 1

                form_data = {
                    'nome': 'NovoNome',
                    'email': 'novonome@email.com',
                    'senha': 'NovaSenha',
                    'adm': 'on'

                }

                response = client.post('/adm/1/atualizar', data=form_data, follow_redirects=True)

                self.assertEqual(response.status_code, 200)

                decoded_response = response.data.decode('utf-8')
                print(decoded_response)

                with app.app_context():
                    user = Usuario.query.get(1)
                    self.assertIsNotNone(user)
                    if user:
                        self.assertEqual(user.nome, 'NovoNome')
                        self.assertEqual(user.email, 'novonome@email.com')

    def test_deleta_usuario_como_adm(self):
        user = Usuario(nome='test_user', senha='senha_de_teste', email='email@email.com', adm=True)
        login_user(user)

        usuario = Usuario.query.get(id)
        if usuario is not None and usuario.adm:
            with app.test_client() as client:
                # Simulando um usuário com permissões de administrador logado
                user = Usuario(nome='admin_user', senha='senha_admin', email='admin@email.com', adm=True)
                login_user(user)

                with client.session_transaction() as sess:
                    sess['user_id'] = 1  # Definir o ID de um usuário com permissões de administração

                # Simulando a exclusão de um usuário com ID 2
                response = client.get('/adm/2/deletar', follow_redirects=True)

                self.assertEqual(response.status_code, 200)
                decoded_response = response.data.decode('utf-8')
                self.assertIn('Usuário Deletado com Sucesso!!', decoded_response)

                # Verificar se o usuário foi excluído do banco de dados
                with app.app_context():
                    deleted_user = Usuario.query.get(2)  # Verificar se o usuário com ID 2 foi excluído
                    self.assertIsNone(deleted_user)

class TestGrafico(unittest.TestCase):
    def setUp(self):

        self.nome_cidade_teste = 'Itambaracá'


        self.grafico = Grafico_1(self.nome_cidade_teste)

    def test_grafico_plot_retorna_dataframe(self):
 
        df = self.grafico.grafico_plot()
        self.assertIsInstance(df, pd.DataFrame, msg="O método não retornou um DataFrame.")

    def test_grafico_plot_colunas_corretas(self):

        df = self.grafico.grafico_plot()
        colunas_esperadas = ['Ano', 'Valores Previstos (Passado)', 'Valores Reais', 'Valores Previstos (Futuros)']
        self.assertListEqual(df.columns.tolist(), colunas_esperadas, msg="O DataFrame não possui as colunas esperadas.")


if __name__ == '__main__':
    unittest.main()