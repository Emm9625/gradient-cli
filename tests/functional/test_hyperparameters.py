import mock
from click.testing import CliRunner

import paperspace.client
from paperspace.cli import cli
from tests import MockResponse, example_responses


class TestCreateHyperparameters(object):
    URL = "https://services.paperspace.io/experiments/v1/hyperopt/"
    COMMAND = [
        "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "pr4yxj956",
    ]
    EXPECTED_REQUEST_JSON = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "some command",
        "workerCount": 1,
        "workerCommand": "some worker command",
        "projectHandle": "pr4yxj956",
    }

    COMMAND_WHEN_ALL_PARAMETERS_WERE_USED = [
        "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "pr4yxj956",
        "--serverRegistryUsername", "someHyperparameterServerRegistryUsername",
        "--serverRegistryPassword", "someHyperparameterServerRegistryPassword",
        "--serverContainerUser", "someHyperparameterServerContainerUser",
    ]
    EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "some command",
        "workerCount": 1,
        "workerCommand": "some worker command",
        "projectHandle": "pr4yxj956",
        "hyperparameterServerRegistryUsername": "someHyperparameterServerRegistryUsername",
        "hyperparameterServerRegistryPassword": "someHyperparameterServerRegistryPassword",
        "hyperparameterServerContainerUser": "someHyperparameterServerContainerUser",
    }
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_RESPONSE = {"handle": "eshgvasywz9k1w", "message": "success"}
    EXPECTED_STDOUT = "Hyperparameter created with ID: eshgvasywz9k1w\n"

    EXPECTED_RESPONSE_JSON_WITH_ERROR = {
        "details": {
            "projectHandle": ["Missing data for required field."],
        },
        "error": "Experiment data error",
    }
    EXPECTED_STDOUT_WHEN_ERROR_RECEIVED = "Experiment data error\nprojectHandle: Missing data for required field.\n"

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "pr4yxj956",
        "--apiKey", "some_key",
    ]
    EXPECTED_REQUEST_JSON_WHEN_API_KEY_PARAMETERS_WAS_USED = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "some command",
        "workerCount": 1,
        "workerCommand": "some worker command",
        "projectHandle": "pr4yxj956",
    }

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"details": "Incorrect API Key provided", "error": "Forbidden"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Forbidden\nIncorrect API Key provided\n"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_get_request_and_print_proper_message_when_create_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_get_request_and_print_proper_message_when_create_command_was_used_with_all_options(self,
                                                                                                            post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WHEN_ALL_PARAMETERS_WERE_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("paperspace.client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_proper_message_when_error_message_received(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WITH_ERROR, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_RECEIVED

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_request_and_print_proper_message_when_error_code_returned_without_json_data(self,
                                                                                                     post_patched):
        post_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None)

        assert result.output == "Unknown error while creating hyperparameter\n"
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestHyperparametersList(object):
    URL = "https://services.paperspace.io/experiments/v1/hyperopt/"
    COMMAND = ["hyperparameters", "list"]
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_REQUEST_PARAMS = {"limit": -1}

    COMMAND_WITH_API_KEY_PARAMETER_USED = ["hyperparameters", "list", "--apiKey", "some_key"]

    EXPECTED_RESPONSE_JSON_WHEN_NO_OBJECTS_WERE_FOUND = {
        "data": [],
        "message": "success",
        "meta": {
            "filter": [],
            "limit": 11,
            "offset": 0,
            "totalItems": 0,
        },
    }

    EXPECTED_STDOUT = """+-----------+----------------+------------+
| Name      | ID             | Project ID |
+-----------+----------------+------------+
| some_name | es3dn6fu16r4kk | pr4yxj956  |
| some_name | eshlqek7wzvrxa | pr4yxj956  |
| some_name | esdwnui5qsk8qm | pr4yxj956  |
| some_name | eshz1z9k37w4nm | pr4yxj956  |
+-----------+----------------+------------+
"""

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 401, "message": "No such API token"}

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_get_request_and_print_list_of_hyperparameters(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_HYPERPARAMETERS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("paperspace.client.requests.get")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_HYPERPARAMETERS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_objects_were_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_OBJECTS_WERE_FOUND, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == "No data found\n"

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == "No such API token\n"
