import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()

client = openai.OpenAI()
model = "gpt-4-turbo"

# # == Create our Assistant ==
# personal_trainer_assis = client.beta.assistants.create(
#     name="Personal Trainer",
#     instructions="You are the best personal trainer and nutritionists. You've trained high caliber athletes and mavoes stars",
#     model=model
# )
# assistant_id = personal_trainer_assis.id
# print(personal_trainer_assis.id)


# # === Thread ===
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "How do I get started working out to lose fat and build muscle at 45yrs old?"
#         }
#     ]
# )
# thread_id = thread.id
# print(thread_id)

# === Hardcode our ids ===
assistant_id = "asst_o3y4aPGZtvjMUGevuyEUwt2C"
thread_id = "thread_Co0MeSaWCrNTUXxoizW4jHsg"

# === Create a Message ===
message = "What should I do to add muscle mass?"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

# === Run our Assistant ===
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Dr Gonzo"
)


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")

                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run.id
)
print("")
print(f"Steps---> {run_steps.data[0]}")
