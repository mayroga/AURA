import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  Alert,
  Switch,
  ScrollView
} from "react-native";

import { styles } from "./styles";
import { ALLOWED_STATES, DISCLAIMER_SHORT } from "./standards";
import { API_URL, PLANS } from "./config";
import { getEstimate, getProviders } from "./api";

export default function App() {
  const [accepted, setAccepted] = useState(false);

  const [state, setState] = useState("");
  const [zip, setZip] = useState("");
  const [code, setCode] = useState("");

  const [insured, setInsured] = useState(false);
  const [planType, setPlanType] = useState("BASIC");

  const [estimate, setEstimate] = useState(null);
  const [providers, setProviders] = useState([]);

  async function handleEstimate() {
    if (!accepted) {
      Alert.alert("Legal notice", "You must accept the disclaimer.");
      return;
    }

    if (!state || !zip || !code) {
      Alert.alert("Missing data", "Please complete all fields.");
      return;
    }

    const data = await getEstimate({
      state,
      zip,
      code,
      insured,
      plan_type: planType
    });

    setEstimate(data);
    setProviders([]);
  }

  async function handleProviders() {
    if (!state || !zip) {
      Alert.alert("Missing data", "State and ZIP are required.");
      return;
    }

    const data = await getProviders({
      state,
      zip
    });

    setProviders(data);
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>
        Healthcare & Dental Cost Transparency
      </Text>

      {/* LEGAL ACCEPTANCE */}
      <View style={styles.legalBox}>
        <Text style={styles.legalText}>
          This platform provides cost estimates only. It does NOT provide
          medical advice, insurance advice, billing, or price guarantees.
        </Text>
        <Button
          title={accepted ? "Disclaimer Accepted ✅" : "Accept Disclaimer"}
          onPress={() => setAccepted(true)}
        />
      </View>

      {/* LOCATION */}
      <TextInput
        placeholder="State (ex: FL)"
        value={state}
        onChangeText={setState}
        style={styles.input}
      />

      <TextInput
        placeholder="ZIP Code"
        value={zip}
        onChangeText={setZip}
        keyboardType="numeric"
        style={styles.input}
      />

      {/* PROCEDURE CODE */}
      <TextInput
        placeholder="Procedure Code (CPT / CDT)"
        value={code}
        onChangeText={setCode}
        style={styles.input}
      />

      {/* INSURANCE */}
      <View style={styles.row}>
        <Text>Insured</Text>
        <Switch value={insured} onValueChange={setInsured} />
      </View>

      {/* PLAN TYPE */}
      <Text style={styles.subtitle}>Plan</Text>
      <View style={styles.row}>
        <Button title="BASIC" onPress={() => setPlanType("BASIC")} />
        <Button title="PAY" onPress={() => setPlanType("PAY_PER_USE")} />
        <Button title="PREMIUM" onPress={() => setPlanType("PREMIUM")} />
      </View>

      <Button title="Get Cost Estimate" onPress={handleEstimate} />

      {/* RESULTS */}
      {estimate && (
        <View style={styles.resultBox}>
          <Text style={styles.resultTitle}>Estimated Cost Range</Text>
          <Text style={styles.resultValue}>
            ${estimate.min} – ${estimate.max}
          </Text>
          <Text>
            {insured ? "Insured" : "Uninsured"} | Plan: {estimate.plan_type}
          </Text>
          <Text style={styles.disclaimer}>{DISCLAIMER_SHORT}</Text>

          <Button
            title="Find Local Providers"
            onPress={handleProviders}
          />
        </View>
      )}

      {/* PROVIDERS */}
      {providers.map((p) => (
        <View key={p.id} style={styles.providerBox}>
          <Text style={styles.providerName}>{p.name}</Text>
          <Text>
            {p.specialty} | ZIP {p.zip}
          </Text>
          <Text>
            {p.in_network ? "In-Network" : "Out-of-Network"}
          </Text>
          <Button
            title="Contact Provider"
            onPress={() =>
              Alert.alert(
                "Contact",
                "Contact this provider directly. Prices are not guaranteed."
              )
            }
          />
        </View>
      ))}
    </ScrollView>
  );
}
