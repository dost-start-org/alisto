import { Stack } from 'expo-router';

export default function AppLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      {/* The Stack navigator will automatically find and include all
        the other files in this directory as screens. You don't 
        need to list them manually like before.
      */}
    </Stack>
  );
}