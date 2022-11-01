import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button} from 'react-native';

export default function App() {
  return (

    <View style={styles.container}>
      <Button title="Signup with Google" onPress={() => navigation.navigate('Home')} />
      <Button title="Login with Google" onPress={() => navigation.navigate('Home')} />
      <StatusBar style="auto" />
    </View>
  );

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
