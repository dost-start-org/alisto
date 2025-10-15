import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import RoleChooseScreen from '../screens/RoleChooseScreen';
import UserHomeScreen from '../screens/UserHomeScreen';
import AdminHomeScreen from '../screens/AdminHomeScreen';
import UserLoginScreen from '../screens/UserLoginScreen';

export type RootStackParamList = {
  RoleChoose: undefined;
  UserHome: undefined;
  AdminHome: undefined;
  UserLogin: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

export default function AppNavigator() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="RoleChoose" component={RoleChooseScreen} />
      <Stack.Screen name="UserHome" component={UserHomeScreen} />
      <Stack.Screen name="AdminHome" component={AdminHomeScreen} />
      <Stack.Screen name="UserLogin" component={UserLoginScreen} />
    </Stack.Navigator>
  );
}
