import React, { useState, useEffect, useRef } from "react";
import { View, Text, TextInput, Button, ScrollView } from "react-native";
import { DJANGO_WS_URL } from "../Auth";

const ChatRoom = ({ route }) => {
  const { groupName } = route.params;
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const ws = useRef(new WebSocket(`${DJANGO_WS_URL}/enable-communication/${groupName}/`)).current;

  useEffect(() => {
    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    return () => {
      ws.close();
    };
  }, [groupName]);

  const handleSendMessage = () => {
    if (inputMessage.trim() !== "" && ws.readyState === WebSocket.OPEN) {
      const message = {
        sender: "Your Sender Name",
        time: new Date().toISOString(),
        message: inputMessage.trim(),
        isSentByMe: true // Flag to identify messages sent by the user
      };
      ws.send(JSON.stringify(message));
      setInputMessage("");
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <ScrollView>
        {messages.map((message, index) => (
          <View key={index} style={{ flexDirection: message.isSentByMe ? "row-reverse" : "row", marginVertical: 5 }}>
            <Text style={{ fontWeight: "bold", marginRight: 5 }}>{message.sender}: </Text>
            <Text>{message.message}</Text>
          </View>
        ))}
      </ScrollView>
      <View style={{ flexDirection: "row", alignItems: "center" }}>
        <TextInput
          style={{ flex: 1, borderWidth: 1, borderColor: "gray", borderRadius: 5, paddingHorizontal: 10, marginRight: 10 }}
          value={inputMessage}
          onChangeText={(text) => setInputMessage(text)}
          placeholder="Type your message..."
        />
        <Button title="Send" onPress={handleSendMessage} />
      </View>
    </View>
  );
};

export default ChatRoom;
