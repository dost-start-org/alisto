import React from "react";
import { Dimensions, StyleSheet, View } from "react-native";
import Svg, { Circle } from "react-native-svg";

const { width, height } = Dimensions.get("window");

const COLORS = {
  redMain: "#E63C3C",
  redShade: "#F9BEBE",
  redHighlight: "#F3D8D8",
};

const LAYERS = [
  { 
    color: COLORS.redHighlight, 
    radiusMultiplier: 0.65,
  },
  { 
    color: COLORS.redShade, 
    radiusMultiplier: 0.60,
  },
  { 
    color: COLORS.redMain, 
    radiusMultiplier: 0.55,
  },
];

const WaveBackground: React.FC = () => {
  const solidBackgroundHeight = height * 0.55;
  const visibleWaveHeight = height * 0.60;

  return (
    <View style={styles.container}>
      <View style={[styles.solidBackground, { height: solidBackgroundHeight }]} />

      {LAYERS.map((layer, index) => {
        const radius = width * layer.radiusMultiplier;
        const diameter = radius * 2;
        
        return (
          <Svg
            key={index}
            width={diameter}
            height={diameter}
            style={[
              styles.svg,
              { 
                left: (width - diameter) / 2,
                bottom: -radius + visibleWaveHeight,
              }
            ]}
          >
            <Circle
              cx={radius}
              cy={radius}
              r={radius}
              fill={layer.color}
            />
          </Svg>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    width: "100%",
    height: "100%", 
    overflow: 'hidden',
  },
  solidBackground: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: COLORS.redMain,
    zIndex: 10,
  },
  svg: {
    position: "absolute",
    zIndex: 1,
  },
});

export default WaveBackground;