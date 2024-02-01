
from openai import OpenAI
import re
import streamlit as st

from snowflake_ddl import get_snowflake_ddl
from mask_snowflake_ddl import mask_ddl_info_with_columns
from prompts_test import get_system_prompt
from unmask_sql_query import unmask_response_statement

warehouse = "COMPUTE_WH"
role = "ACCOUNTADMIN"
user = "willcheaquitrial"
password = "Jamie23@marriage"
account = "NADSAKL-XK17589"
database = 'GARDEN_PLANTS'

test = get_snowflake_ddl(account=account, user=user, password=password, warehouse=warehouse, database=database,
                         role=role)

mapped = {}
masked_ddl, mapped['schemas'], mapped['tables'], mapped['columns'] = mask_ddl_info_with_columns(test)

system_prompt = get_system_prompt(context=masked_ddl)

st.title("WitBit")

# Initialize the chat messages history
client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": unmask_response_statement(prompt, mapping=mapped, unmask=False)})
    print(unmask_response_statement(prompt, mapping=mapped, unmask=False))

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(unmask_response_statement(message["content"], mapped))
        if "results" in message:
            st.dataframe(unmask_response_statement(message["results"], mapped))
        print(unmask_response_statement(message["results"], mapped))

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in unmask_response_statement(st.session_state.messages, mapping=mapped, unmask=False)],
            stream=True,
        ):
            response += unmask_response_statement(delta.choices[0].delta.content or "", mapping=mapped)
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1)
            conn = st.connection("snowflake")
            message["results"] = conn.query(sql)
            st.dataframe(message["results"])
        st.session_state.messages.append(message)