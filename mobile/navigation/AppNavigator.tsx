import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import RoleChooseScreen from '../screens/RoleChooseScreen';
import UserHomeScreen from '../screens/UserHomeScreen';
import AdminHomeScreen from '../screens/AdminHomeScreen';
import UserLoginScreen from '../screens/UserLoginScreen';
import EmergencyOptionsScreen from '../screens/EmergencyOptionsScreen';
import LocationSelectScreen from '../screens/LocationSelectScreen';
import ReportingEmergencyScreen from '../screens/ReportingEmergencyScreen';
import NotificationsScreen from '../screens/NotificationsScreen';
import ReportVerifiedScreen from '../screens/ReportVerifiedScreen';

type EmergencyDataObject = {
 key: string;
 label: string;
 title: string;
 icon: any;
};

export type RootStackParamList = {
 RoleChoose: undefined;
 UserHome: undefined;
 AdminHome: undefined;
 UserLogin: undefined;
 EmergencyOptions: undefined;
 LocationSelectScreen: { emergencyData: EmergencyDataObject };
 ReportingEmergencyScreen: { emergencyData: EmergencyDataObject; location: string };
 
 // --- FIX APPLIED HERE: Update ReportVerifiedScreen to accept the parameters it needs ---
 ReportVerifiedScreen: { emergencyData: EmergencyDataObject; location: string };
 // ---------------------------------------------------------------------------------------

 Notifications: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

export default function AppNavigator() {
 return (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
   <Stack.Screen name="RoleChoose" component={RoleChooseScreen} />
   <Stack.Screen name="UserHome" component={UserHomeScreen} />
   <Stack.Screen name="AdminHome" component={AdminHomeScreen} />
   <Stack.Screen name="UserLogin" component={UserLoginScreen} />
   <Stack.Screen name="EmergencyOptions" component={EmergencyOptionsScreen} />
   <Stack.Screen name="LocationSelectScreen" component={LocationSelectScreen} />
   <Stack.Screen name="ReportingEmergencyScreen" component={ReportingEmergencyScreen} />
   <Stack.Screen name="Notifications" component={NotificationsScreen} />
   <Stack.Screen name="ReportVerifiedScreen" component={ReportVerifiedScreen} />
  </Stack.Navigator>
 );
}