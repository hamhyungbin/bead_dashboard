// ... (기존 import 및 함수 상단 부분) ...
import WidgetWrapper from '../components/WidgetWrapper'; // WidgetWrapper 임포트

// ... (DashboardPage 함수 내부) ...

      <ResponsiveGridLayout
        // ... (기존 ResponsiveGridLayout props) ...
      >
        {widgets.map((widget) => (
          <div key={widget.id} data-grid={widget.layout} className="overflow-hidden"> {/* 여기서 bg, shadow, rounded 제거 */}
            <WidgetWrapper widget={widget} onDelete={deleteWidget}>
              {widget.type === 'notes' && (
                <NotesWidget
                  config={widget.config}
                  onSave={(newContent) => updateWidgetConfig(widget.id, { content: newContent })}
                />
              )}
              {widget.type === 'weather' && (
                <WeatherWidget
                  initialCity={widget.config?.city || 'Seoul'}
                  onCityChange={(newCity) => updateWidgetConfig(widget.id, { city: newCity })}
                />
              )}
              {/* 다른 위젯 타입들도 여기에 추가 */}
            </WidgetWrapper>
          </div>
        ))}
      </ResponsiveGridLayout>
// ... (나머지 DashboardPage 함수 부분) ...