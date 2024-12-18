from openai import OpenAI
from configs.settings import settings
import json

openAIClient = OpenAI(
    api_key=settings.openai_key_secret,
)


def query_generator(input: str):
    return input + " generated"


def query_generator_openai(user_input: str, wallet: str):
    system_prompt = (
        "You are a highly specialized RPC assistant for the SWQuery SDK, which enhances Solana RPC functionalities. "
        "The user will provide input in natural language, and your role is to return "
        "ONLY a JSON in the following format:\n"
        "{\n"
        "   \"response\": \"<method_name_or_message>\",\n"
        "   \"params\": {,\n"
        "       \"<param_name>\": <param_value>,\n"
        "       ...\n"
        "   },\n"
        "   \"status\": \"success\" or \"error\"\n"
        "}\n\n"
        "If the user's request can be answered by one of the methods in the list, "
        "return the method name and \"status\": \"success\"."
        "If the method requires parameters, include them in the \"params\" array. And always return too the wallet address as a parameter named as 'address'\n"
        "If the user's request is recognized as a Solana RPC query but no suitable method "
        "is available in the list, return:\n"
        "{\n"
        "   \"response\": \"We recognized your request as a Solana RPC query, but no implemented method is available.\",\n"
        "   \"status\": \"error\"\n"
        "}\n\n"
        "If there is no method that meets the user's request and it doesn't seem to be a Solana RPC query, return:\n"
        "{\n"
        "   \"response\": \"We need your request to be a query to be executed on the Solana network via SWQuery SDK\",\n"
        "   \"status\": \"error\"\n"
        "}\n\n"
        "List of available methods in SWQuery SDK (including parameters):\n"
        "1. getAssetsByCreator(creator: String)\n"
        "2. getAssetsByCreatorFiltered(creator: String, filters: HashMap<String, String>)\n"
        "3. getAssetsByOwner(owner: String)\n"
        "4. getAssetsByOwnerSummary(owner: String)\n"
        "5. getAssetsByAuthority(authority: String)\n"
        "6. getSignaturesForAsset(asset_id: String)\n"
        "7. getSignaturesForAddress(address: String)\n"
        "8. getSignaturesForAddressPeriod(address: String, from: u64, to: u64)\n"
        "9. getRecentTransactions(address: String, days: u8)\n"
        "10. getTransaction(signature: String)\n"
        "11. getTransactionDetails(signatures: Vec<String>)\n"
        "12. isTransactionSuccessful(signature: String)\n"
        "13. getBalance(address: String)\n"
        "14. getTotalBalance(owner: String)\n"
        "15. getTokenAccountBalance(account: String)\n"
        "16. getTokenBalancesForOwner(owner: String, mint: String)\n"
        "17. getTokenLargestAccounts(mint: String)\n"
        "18. getLargestTokenAccounts(mint: String)\n"
        "19. getTokenSupply(mint: String)\n"
        "20. getProgramAccounts(program_id: String)\n"
        "21. getProgramAccountsWithFilters(program_id: String, filters: HashMap<String, String>)\n"
        "22. getBlockHeight()\n"
        "23. getBlockProduction()\n"
        "24. getBlockCommitment(block: u64)\n"
        "25. getBlocks(start_slot: u64, end_slot: u64)\n"
        "26. getBlocksInPeriod(from_slot: u64, to_slot: u64)\n"
        "27. getBlockTime(slot: u64)\n"
        "28. getClusterNodes()\n"
        "29. getActiveValidators()\n"
        "30. getEpochInfo()\n"
        "31. getEpochSchedule()\n"
        "32. getFeeForMessage(message: String)\n"
        "33. getFeeStatistics(blocks: Vec<u64>)\n"
        "34. getFirstAvailableBlock()\n"
        "35. getGenesisHash()\n"
        "36. getHealth()\n"
        "37. getHighestSnapshotSlot()\n"
        "38. getIdentity()\n"
        "39. getInflationGovernor()\n"
        "40. getInflationRate()\n"
        "41. getLargestAccounts()\n"
        "42. getLatestBlockhash()\n"
        "43. getLeaderSchedule()\n"
        "44. getLeaderScheduleSummary()\n"
        "45. getMaxRetransmitSlot()\n"
        "46. getMaxShredInsertSlot()\n"
        "47. getMinimumBalanceForRentExemption(size: u64)\n"
        "48. getRecentPerformanceSamples()\n"
        "49. getSlot()\n"
        "50. getSlotLeader()\n"
        "51. getStakeActivation(account: String, epoch: Option<u64>)\n"
        "52. getStakeMinimumDelegation()\n"
        "53. getSupply()\n"
        "54. isBlockhashValid(blockhash: String)\n"
        "55. minimumLedgerSlot()\n"
        "56. getAccountInfo(account: String)\n"
        "57. monitorAddress(address: String, interval: u64, callback: Function)\n"
        "\nIf the user's query matches any of the above methods, return its name in the JSON response "
        "with \"status\": \"success\". Otherwise, follow the error-handling logic provided."
    )

    response = openAIClient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"My wallet address is {wallet}"},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"}
    )

    promptResult = response.choices[0].message.content.strip()

    promptResult = json.loads(promptResult)

    return {
        "result": promptResult,
        "tokens": response.usage.total_tokens
    }


def generate_visualization(input: str):
    # system_prompt = (
    #     "You are a highly specialized RPC assistant for the SWQuery SDK, which enhances Solana RPC functionalities. "
    #     "You will be provided with a JSON in a varying format, and your role is to return a Markdown visualization of the data.\n"
    #     "You can use the following Markdown syntax to create a table:\n"
    #     "| Header 1 | Header 2 |\n"
    #     "| -------- | -------- |\n"
    #     "| Cell 1   | Cell 2   |\n"
    #     "\n"
    #     "You can use the following Markdown syntax to create a list:\n"
    #     "- Item 1\n"
    #     "- Item 2\n"
    #     "\n"
    #     "You can use the following Markdown syntax to create a link:\n"
    #     "[Link text](https://www.example.com)\n"
    #     "\n"
    # )
    # Salvei oq jamanta

    system_prompt = (
        "Você é um agente LLM especializado em interações com blockchain, "
        "especificamente com a Solana. Você utiliza JSONs retornados por chamadas "
        "RPC feitas pela API da Helius para gerar resumos claros e organizados. "
        "\n\n"
        "Contexto: "
        "\n"
        "O Remote Procedure Call (RPC) é um método que permite executar operações em um "
        "servidor remoto como se fossem funções locais. Na blockchain Solana, chamadas "
        "RPC são amplamente utilizadas para consultar dados sobre transações, contas, "
        "estados de programas, eventos e outros dados da rede. "
        "\n"
        "A Helius é uma API que simplifica a interação com a Solana, fornecendo ferramentas "
        "para acessar dados complexos de maneira eficiente. Por meio dela, os desenvolvedores "
        "podem consultar informações como transações, logs, estados de contas e eventos, o que "
        "facilita o desenvolvimento de aplicações baseadas na blockchain."
        "\n\n"
        "Sua tarefa é transformar o JSON retornado por chamadas RPC em um resumo em Markdown, "
        "extraindo e organizando as informações mais relevantes. Considere o seguinte ao gerar o resumo:"
        "\n\n"
        "1. Identifique os dados mais importantes presentes no JSON, como transações, "
        "contas, tokens, logs de eventos, programas ou estados."
        "\n"
        "2. Estruture o resumo em Markdown com as seguintes seções (se aplicáveis): "
        "   - **Resumo Geral:** Descrição breve do conteúdo do JSON. "
        "   - **Principais Campos:** Destaque os campos mais relevantes e seus valores. "
        "   - **Entidades ou Contas Envolvidas:** Liste contas, programas ou entidades mencionadas, "
        "     incluindo detalhes relevantes como saldos ou identificadores. "
        "   - **Eventos ou Logs:** Apresente logs, mensagens ou eventos destacados, se existirem. "
        "   - **Outras Informações:** Qualquer dado adicional relevante que não se encaixe nas seções acima."
        "\n"
        "3. Ignore informações redundantes ou irrelevantes para um resumo."
        "4. Se o JSON for extenso, priorize apenas os dados mais significativos."
        "\n\n"
        "Certifique-se de manter a organização lógica, clareza e incluir apenas informações "
        "que agreguem valor ao entendimento do conteúdo."
    )

    response = openAIClient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input}
        ],
        response_format={"type": "json_object"}
    )

    promptResult = response.choices[0].message.content.strip()

    return {
        "result": promptResult,
        "tokens": response.usage.total_tokens
    }
