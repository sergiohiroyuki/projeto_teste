import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hello import app, Usuario, Historico, db
import pandas as pd

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senha@localhost/atividade_teste'
        app.app_context()
        db.create_all()
        self.app = app.test_client()

    def create_all_tables(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_selecionar_todos_usuarios(self):
        with app.app_context():
            user1 = Usuario(nome='TestUser1', email='testuser1@example.com', senha='password1', adm=False)
            user2 = Usuario(nome='TestUser2', email='testuser2@example.com', senha='password2', adm=True)

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        response = self.app.get('/adm')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestUser1', response.data)
        self.assertIn(b'TestUser2', response.data)

    def test_selecionar_um_usuario(self):
        user = Usuario(nome='TestUser', email='testuser@example.com', senha='password', adm=False)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.get('/adm/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestUser', response.data)

    def test_criar_usuario(self):
        data = {
            'nome': 'NewUser',
            'email': 'newuser@example.com',
            'senha': 'newpassword',
            'confirmar_senha': 'newpassword',
            'adm_cadastrar': 'on'
        }

        response = self.app.post('/adm/cadastrar', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with app.app_context():
            user = Usuario.query.filter_by(nome='NewUser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.adm, True)

    def test_atualiza_usuario(self):
        user = Usuario(nome='TestUser', email='testuser@example.com', senha='password', adm=False)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        data = {
            'nome': 'UpdatedUser',
            'email': 'updateduser@example.com',
            'senha': 'newpassword',
            'adm_alterar': 'on'
        }

        response = self.app.post('/adm/1/atualizar', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        updated_user = Usuario.query.get(1)
        self.assertEqual(updated_user.nome, 'UpdatedUser')
        self.assertEqual(updated_user.email, 'updateduser@example.com')
        self.assertEqual(updated_user.adm, True)

    def test_deleta_usuario(self):
        user = Usuario(nome='TestUser', email='testuser@example.com', senha='password', adm=False)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.get('/adm/1/deletar', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        deleted_user = Usuario.query.get(1)
        self.assertIsNone(deleted_user)

    
    def test_login_confirmado(self):
        with self.app as client:
            response = client.post('/login', data=dict(nome='example_user', senha='example_password'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_login_falha(self):
        with self.app as client:
            response = client.post('/login', data=dict(nome='nonexistent_user', senha='wrong_password'), follow_redirects=True)
            self.assertIn(b'Verifique o Nome ou a Senha!!', response.data)

    def test_logout(self):
        with self.app as client:
            response = client.get('/logout', follow_redirects=True)
            self.assertIn(b'Usu\u00e1rio Saiu da Aplica\u00e7\u00e3o com Sucesso!!', response.data)

    def test_grafico_plot_retorna_dataframe(self):
        resultado = self.grafico.grafico_plot()
        self.assertIsInstance(resultado, pd.DataFrame)

    def test_grafico_plot_existente(self):
        resultado = self.grafico.grafico_plot()
        self.assertIsNotNone(resultado) 

    def test_grafico_plot_inexistente(self):
        grafico_inexistente = Grafico_1(self.nome_cidade_inexistente)
        resultado = grafico_inexistente.grafico_plot()
        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
