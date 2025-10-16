import React, { useState } from 'react';
import { View, StyleSheet, ViewStyle, LayoutChangeEvent } from 'react-native';

const GRID_COLOR = '#000000';
const GRID_OPACITY = 0.08;
const LINE_SPACING = 40;
const GRID_PADDING = 10;

interface GridBackgroundProps {
  style?: ViewStyle;
  height: number;
}

const GridBackground: React.FC<GridBackgroundProps> = ({ style, height }) => {
  const [containerWidth, setContainerWidth] = useState(0);

  const onLayout = (event: LayoutChangeEvent) => {
    const { width } = event.nativeEvent.layout;
    if (width !== containerWidth) {
      setContainerWidth(width);
    }
  };

  const renderGrid = containerWidth > 0;
  
  const availableWidth = containerWidth - 2 * GRID_PADDING;
  const effectiveHeight = height - 2 * GRID_PADDING;

  const intervalsFit = Math.ceil(availableWidth / LINE_SPACING); 
  const patternWidth = intervalsFit * LINE_SPACING;
  const centeringSpace = patternWidth - availableWidth;
  const centeringOffset = centeringSpace / 2;

  const verticalLines = Array.from({ length: intervalsFit + 1 }, (_, i) => i);

  const horizontalLineCount = Math.floor(effectiveHeight / LINE_SPACING); 
  const horizontalLines = Array.from({ length: horizontalLineCount - 1 }, (_, i) => i + 1);

  return (
    <View style={[styles.gridContainer, { height }, style]} onLayout={onLayout}>
      
      <View style={styles.paddingWrapper}>
        
        {renderGrid && (
          <View style={[styles.centeringWrapper, { left: -centeringOffset, width: patternWidth }]}> 
            
            {horizontalLines.map((i) => (
                <View
                    key={`h-${i}`}
                    style={[
                        styles.gridLine,
                        styles.horizontalLine,
                        { top: i * LINE_SPACING },
                    ]}
                />
            ))}

            {verticalLines.map((i) => (
                <View
                    key={`v-${i}`}
                    style={[
                        styles.gridLine,
                        styles.verticalLine,
                        { left: i * LINE_SPACING },
                    ]}
                />
            ))}
          </View>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  gridContainer: {
    overflow: 'hidden',
    position: 'absolute',
    width: '100%',
  },
  paddingWrapper: {
    position: 'absolute',
    top: GRID_PADDING,
    left: GRID_PADDING,
    right: GRID_PADDING,
    bottom: GRID_PADDING,
    overflow: 'hidden',
  },
  centeringWrapper: {
    position: 'absolute',
    top: 0,
    height: '100%',
  },
  lineBase: {
    position: 'absolute',
  },
  gridLine: {
    position: 'absolute',
    borderColor: GRID_COLOR,
    borderStyle: 'solid',
    opacity: GRID_OPACITY,
    zIndex: -1,
  },
  horizontalLine: {
    borderBottomWidth: 1,
    width: '100%', 
  },
  verticalLine: {
    borderLeftWidth: 1,
    height: '100%',
  }
});

export default GridBackground;