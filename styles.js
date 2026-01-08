import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#f7f7f7"
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 15,
    textAlign: "center"
  },
  subtitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginTop: 10
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    marginVertical: 5,
    borderRadius: 5,
    backgroundColor: "#fff"
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginVertical: 5
  },
  legalBox: {
    backgroundColor: "#fff3cd",
    padding: 10,
    marginBottom: 15,
    borderRadius: 5
  },
  legalText: {
    fontSize: 12,
    color: "#333",
    marginBottom: 5
  },
  resultBox: {
    backgroundColor: "#fff",
    padding: 15,
    marginTop: 15,
    borderRadius: 5,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1,
    elevation: 2
  },
  resultTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 5
  },
  resultValue: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#0b5cff",
    marginBottom: 5
  },
  disclaimer: {
    fontSize: 10,
    color: "#555",
    marginTop: 5
  },
  providerBox: {
    backgroundColor: "#e2f0fb",
    padding: 10,
    marginTop: 10,
    borderRadius: 5
  },
  providerName: {
    fontWeight: "bold",
    fontSize: 14
  }
});
