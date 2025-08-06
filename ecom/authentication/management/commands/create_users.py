import random
from django.core.management.base import BaseCommand
from authentication.models import CustomUser

class Command(BaseCommand):
    help = 'Créer 20 utilisateurs CustomUser différents avec noms/prénoms du Burkina Faso'

    def handle(self, *args, **kwargs):
        noms_bf = [
            'BADOLO', 'FOFANA', 'KONSIAGRI', 'KABORE', 'OUEDRAGO', 
            'ZONGO', 'DIAWARA', 'SANKARA', 'OUATTARA', 'THIEBA',
            'BILGO', 'SANOU', 'TRAORE', 'DABIRE', 'BONKOUARA',
            'TOURE', 'NACDIA', 'COULIBALY', 'DAO', 'SORE'
        ]

        prenoms_bf = [
            'Yadia', 'Souley', 'Fatim', 'Jeremie', 'Aminata', 
            'Moussa', 'Adama', 'Salif', 'Zeinabou', 'Ibrahim',
            'Mariama', 'Seydou', 'Hadja', 'Ousmane', 'Rokia',
            'Issa', 'Nafissatou', 'Boubacar', 'Kadiatou', 'Soumaila'
        ]

        roles = [CustomUser.Role.CLIENT, CustomUser.Role.VENDEUR, CustomUser.Role.ADMIN]
        statuses = [CustomUser.Status.ACTIF, CustomUser.Status.INACTIF, CustomUser.Status.SUSPENDU]

        created_count = 0

        for i in range(20):
            prenom = random.choice(prenoms_bf)
            nom = random.choice(noms_bf)
            username = f'{prenom.lower()}{i+1}'
            email = f'{prenom.lower()}{nom.lower()}{i+1}@example.com'
            telephone = f'+226{random.randint(70000000, 79999999)}'  # numéro burkinabé fictif
            role = roles[i % len(roles)]
            status = statuses[i % len(statuses)]
            password = 'Test1234!'  # mot de passe par défaut

            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(f'Utilisateur avec email {email} existe déjà, skip.')
                continue

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                role=role,
                status=status,
                password=password,
            )

            self.stdout.write(self.style.SUCCESS(f'Créé utilisateur : {email} ({role})'))
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Total utilisateurs créés : {created_count}'))
