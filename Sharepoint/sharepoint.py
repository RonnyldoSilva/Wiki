import logging

from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
from io import BytesIO
import pandas as pd

try:
    from utils import SharePointConfig
except ImportError:
    from functions.process_create_chat.utils import SharePointConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SharepointConnector:
    def __init__(
        self, url: str, site: str, folder: str, client_id: str, client_secret: str
    ):
        self.url = url
        self.site = site
        self.folder = folder
        self.client_id = client_id
        self.client_secret = client_secret

    def get_context(self):
        logger.info(f"Authenticating to SharePoint...")
        site_url = self.url + self.site
        ctx_auth = AuthenticationContext(site_url)
        ctx_auth.acquire_token_for_app(self.client_id, self.client_secret)
        return ClientContext(site_url, ctx_auth)

    def download_file(self, file_name: str, sub_folder: str = "") -> bytes:
        ctx = self.get_context()
        file_url = self.site + self.folder + sub_folder + file_name

        logger.info(f"Downloading {file_url}")
        file_content = File.open_binary(ctx, file_url).content

        return file_content

    def upload_file(self, file_content: bytes, file_name: str, sub_folder: str = ""):
        ctx = self.get_context()
        file = (
            ctx.web.get_folder_by_server_relative_url(self.folder + sub_folder)
            .upload_file(file_name, file_content)
            .execute_query()
        )
        return file

    def upload_csv_from_df(self, files):
        for name, content in files.items():
            file = content.replace(
                to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" ", " "], regex=True
            ).to_csv(index=False, sep=";")
            self.upload_file(bytes(file, "utf-8"), name)

    def download_excel_to_df(self, name: str, path: str, worksheet_name: str):
        file = self.download_file(name, path)

        return pd.read_excel(BytesIO(file), sheet_name=worksheet_name)


def download_contacts_df(
    sharepoint_conf: SharePointConfig, file_name: str, worksheet_name: str
) -> pd.DataFrame:
    """
    Faz o download do arquivo excel com contatos e categorias de e-mails para alertas e converte para df
    """
    sp = SharepointConnector(
        url=sharepoint_conf.url,
        site=sharepoint_conf.site,
        folder=sharepoint_conf.folder,
        client_id=sharepoint_conf.client_id,
        client_secret=sharepoint_conf.client_secret,
    )

    df_word = sp.download_excel_to_df(file_name, "", worksheet_name=worksheet_name)
    return df_word
