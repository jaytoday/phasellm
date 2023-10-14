import httpx

from warnings import warn

from openai import OpenAI

from abc import ABC, abstractmethod

from azure.identity import DefaultAzureCredential


class APIConfiguration(ABC):

    def __init__(self, model: str = 'gpt-3.5-turbo'):
        self.model = model

    @abstractmethod
    def __call__(self):
        """
        Abstract method to initialize the API configuration.

        Returns:

        """
        pass

    @abstractmethod
    def get_base_api_kwargs(self):
        """
        Abstract method for the base API kwargs for the API configuration.

        Returns:

        """
        pass


class OpenAIConfiguration(APIConfiguration):
    name = 'openai'

    def __init__(
            self,
            api_key: str,
            organization: str = None,
            model: str = 'gpt-3.5-turbo',
            response_callback: callable = lambda response: None
    ):
        """
        Initializes the OpenAI API configuration.

        Args:
            api_key: The OpenAI API key.
            organization: The OpenAI organization.
            model: The model to use.
            response_callback: A callback which is called when a response is received from the OpenAI API.

        """
        super().__init__(model=model)

        self.api_key = api_key
        self.organization = organization

        self._response_callback = response_callback

    def __call__(self):
        """
        Calls the OpenAI API configuration to initialize the OpenAI API.

        Returns:

        """
        self.client = OpenAI(
            http_client=httpx.Client(event_hooks={'response': [self._response_callback]}),
            api_key=self.api_key,
            organization=self.organization
        )

    def get_base_api_kwargs(self):
        """
        Returns the base API kwargs for the OpenAI API configuration.

        Returns:
            A Dict of the base API kwargs for the OpenAI API configuration.

        """
        return {
            'model': self.model
        }


class AzureAPIConfiguration(APIConfiguration):
    name = 'azure'

    def __init__(
            self,
            api_key: str,
            base_url: str = None,
            api_version: str = '2023-05-15',
            deployment_id: str = 'gpt-3.5-turbo',
            response_callback: callable = lambda response: None,
            api_base: str = None
    ):
        """
        Initializes the Azure API configuration.

        Args:
            api_key: The Azure API key.
            base_url: The Azure API base URL.
            api_version: The Azure API version.
            deployment_id: The model deployment ID.
            response_callback: A callback which is called when a response is received from the Azure API.
            api_base: (DEPRECATED) The Azure API base.

        """
        super().__init__(model=deployment_id)

        if api_base:
            warn('The api_base argument is deprecated. Use base_url instead.', DeprecationWarning)

        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        if api_base:
            self.base_url = api_base

        self.deployment_id = deployment_id

        self._response_callback = response_callback

    def __call__(self):
        """
        Calls the Azure API configuration to initialize the Azure API.

        Returns:

        """
        # Reset the OpenAI API configuration.
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_query={
                'api-version': self.api_version
            },
            default_headers={
                'api-key': self.api_key
            },
            http_client=httpx.Client(event_hooks={'response': [self._response_callback]}),
        )

    def get_base_api_kwargs(self):
        """
        Returns the base API kwargs for the Azure API configuration.

        Returns:
            A Dict of the base API kwargs for the Azure API configuration.

        """
        return {
            'model': self.deployment_id
        }


class AzureActiveDirectoryConfiguration:
    name = 'azure_ad'

    def __init__(
            self,
            base_url: str,
            api_version: str = '2023-05-15',
            deployment_id: str = 'gpt-3.5-turbo',
            response_callback: callable = lambda response: None,
            api_base: str = None
    ):
        """
        Initializes the Azure Active Directory API configuration.

        Learn more:
        https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints#azure-active-directory-authentication

        Args:
            base_url: The Azure Active Directory API base.
            api_version: The API version. https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
            deployment_id: The model deployment ID
            response_callback: A callback which is called when a response is received from the Azure Active Directory API.
            api_base: (DEPRECATED) The Azure Active Directory API base.

        """
        super().__init__(model=deployment_id)

        if api_base:
            warn('The api_base argument is deprecated. Use base_url instead.', DeprecationWarning)

        self.base_url = base_url
        if api_base:
            self.base_url = api_base

        self.api_version = api_version
        self.deployment_id = deployment_id

        self._response_callback = response_callback

    def __call__(self):
        """
        Calls the Azure Active Directory API configuration to initialize the Azure Active Directory API.

        Returns:

        """

        # Set the OpenAI API configuration.
        credential = DefaultAzureCredential()
        token = credential.get_token('https://cognitiveservices.azure.com/.default')

        # Reset the OpenAI API configuration.
        self.client = OpenAI(
            api_key=token.token,
            base_url=self.base_url,
            http_client=httpx.Client(event_hooks={'response': [self._response_callback]}),
            default_query={
                'api-version': self.api_version
            }
        )

    def get_base_api_kwargs(self):
        """
        Returns the base API kwargs for the Azure Active Directory API configuration.

        Returns:
            A Dict containing the base API kwargs for the Azure Active Directory API configuration.

        """
        return {
            'deployment_id': self.deployment_id
        }
