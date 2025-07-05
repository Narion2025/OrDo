import voice_config\nfrom elevenlabs import generate, save, set_api_key

set_api_key("sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28")


audio = generate(text="Dies ist ein Test der echten Stimme.", voice=voice_config.VOICE_ID_NIETZSCHE, model="eleven_multilingual_v2")
save(audio, "/tmp/eleven_test.mp3")
print("✔️ Audio gespeichert: /tmp/eleven_test.mp3")

