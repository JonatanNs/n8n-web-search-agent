import requests
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        N8N_WEBHOOK_URL: str = Field(default="", description="URL du webhook n8n")
        N8N_WEBHOOK_TOKEN: str = Field(default="", description="Token X-Webhook-Token")
        TIMEOUT: int = Field(default=20, description="Délai max de la requête (secondes)")

    def __init__(self):
        self.valves = self.Valves()

    def chercher_sur_le_web(self, query: str) -> str:
        """
        Recherche des informations récentes sur internet.
        Utilise cet outil quand la question porte sur l'actualité ou sur
        des informations que tu ne connais pas avec certitude.

        :param query: la question ou les mots-clés à rechercher sur le web
        :return: un JSON contenant une réponse synthétique et les sources (titre, url, extrait)
        """
        if not self.valves.N8N_WEBHOOK_URL:
            return "Erreur de configuration : l'URL du webhook n8n n'est pas renseignée dans les Valves."

        try:
            response = requests.post(
                self.valves.N8N_WEBHOOK_URL,
                json={"query": query},
                headers={"X-Webhook-Token": self.valves.N8N_WEBHOOK_TOKEN},
                timeout=self.valves.TIMEOUT,
            )
        except requests.Timeout:
            return "Erreur : la recherche web a pris trop de temps. Réessaie avec une question plus précise."
        except requests.ConnectionError:
            return "Erreur : impossible de joindre n8n. Vérifie que n8n est bien démarré."

        if response.status_code == 200:
            return response.text
        if response.status_code == 403:
            return "Erreur : accès refusé par n8n. Vérifie le token dans les Valves."
        if response.status_code == 502:
            return f"Erreur : la recherche Tavily a échoué. Détails : {response.text}"

        return f"Erreur inattendue de n8n ({response.status_code}) : {response.text}"