API를 구현할 때, 날짜와 시간 값을 교환하는 쉬운 방법을 정리했습니다.

## 개요

Spring MVC framework 기반에서 API를 개발할 때, 클라이언트에서 전달 받는 날짜 및 시간 문자열 값을 프로젝트 레벨에서 적용하는 방법을 공유하고자 이 글을 작성했습니다. 

## 잘못된 방식

기존에는 아래와 같이 String 타입으로 날짜와 시간 값을 받아 처리했었습니다. 

```java
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public static class SaveReq {

    private String deadline;

    public Coverletter toEntity() {
        return Coverletter.builder()
                .deadline(new Deadline(deadline))
                .build();
    }
}

@Embeddable
public class Deadline {

    @Getter
    @Column(name = "deadline")
    private LocalDateTime deadline;

    private final static String DATETIME_FORMAT = "yyyy-MM-dd HH:mm";

    public Deadline() {
        this.deadline = null;
    }

    public Deadline(String datetimeStr) {
        if (datetimeStr == null || datetimeStr.isEmpty()) {
            this.deadline = null;
            return;
        }

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(DATETIME_FORMAT);
        this.deadline = LocalDateTime.parse(datetimeStr, formatter);
    }
}
```

위와 같이 우선 날짜 값을 문자열로 받고, 날짜 데이터가 필요한 Deadline 클래스에서 해당 날짜값의 포멧이 올바른지 검증하는 형태로 구현했습니다. 만약 다른 곳에서도 포멧을 검증해야 한다면, 비슷한 로직의 중복이 발생하게 되는 문제가 발생합니다. 중복을 방지하기 위해 포멧을 체크하는 별도의 유틸 클래스를 만들어도 되지만, 개발자가 날짜 값을 체크해야 한다는 사실을 망각할 수 있기 때문에, 그다지 효율적인 것 같진 않습니다. 

그래서 날짜 값에 대한 포멧팅을 미리 정의해놓고, API 요청과 응답시 날짜 값에 대한 포멧팅을 강제로 적용하는 법을 찾아봤습니다. 그 결과, Spring에서 제공해주는 Formatter라는 API를 발견했습니다. (pivotal 만세~~)

## Formatter 구현

우선 Formatter API를 소개하겠습니다. Formatter API의 최상위 인터페이스는 Formatter<T>로써, T를 String으로 변환하는 Printer API와 String을 T로 변환하는 API 총 2가지로 구성되어 있습니다.

```java
package org.springframework.format;

public interface Formatter<T> extends Printer<T>, Parser<T> {
}
```

Formatter를 구현하기에 앞서 `구현 목표`를 정의하겠습니다.
- 클라이언트에서 json 타입의 날짜 및 시간 문자열 값을 다음과 같이 보낼 때, 서버에서 그 값을 즉시 LocalDateTime으로 맵핑하기

이 목표를 달성하기 위해 해야할 것은 DatetimeFormatter 클래스를 생성하고 Bean으로 정의하면 됩니다.

```java
@Component
public class LocalDateTimeFormatter implements Formatter<LocalDateTime> {

    private final static String LOCAL_DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss";

    @Override
    public LocalDateTime parse(String text, Locale locale) throws ParseException {
        return LocalDateTime.parse(text, DateTimeFormatter.ofPattern(LOCAL_DATE_TIME_FORMAT));
    }

    @Override
    public String print(LocalDateTime obj, Locale locale) {
        return DateTimeFormatter.ofPattern(LOCAL_DATE_TIME_FORMAT).format(obj);
    }
}
```

이제 Dto를 정의한 뒤, 실제로 잘 작동하는지 확인해보겠습니다.

```java
class TestDto {
    LocalDateTime localDateTime;
}

@RestController
@RequestMapping("/test")
public class TestController {

    @PostMapping
    public void test1(@RequestBody TestDto testDto) {
       return;
    }

    @GetMapping
    public void test2(@ModelAttribute TestDto testDto) {
        return;
    }
}
```

각각 API의 요청 결과는 아래와 같습니다.
- test1 API는 실패, 
- test2 API는 성공. 

이유는 Spring Boot 2.x는 json 타입의 데이터를 수신할 때 jackson library를 기본 값으로 사용합니다. 따라서 json 타입으로 값을 주고 받을 때는 jackson에 별도로 serializer를 구현해야 합니다.


## Serializer 구현

Serializer는 아래와 같이 구현할 수 있습니다. 

```java
public class JacksonFormattingConfig {

	@Bean
	public ObjectMapper objectMapper() {
		ObjectMapper objectMapper = new ObjectMapper();
		objectMapper.registerModule(new Jdk8Module());
		objectMapper.registerModule(jsonMapperJava8DateTimeModule());
		return objectMapper;
	}

	private Module jsonMapperJava8DateTimeModule() {
		SimpleModule module = new SimpleModule();

		module.addDeserializer(LocalDateTime.class, new JsonDeserializer<LocalDateTime>() {
			@Override
			public LocalDateTime deserialize(JsonParser p, DeserializationContext ctxt) throws IOException, JsonProcessingException {
				return LocalDateTime.parse(p.getValueAsString(), DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
			}
		});

		module.addSerializer(LocalDateTime.class, new JsonSerializer<LocalDateTime>() {
			@Override
			public void serialize(LocalDateTime value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
				gen.writeString(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").format(value));
			}
		});
		return module;
	}
}
```

이렇게 한 번 설정해놓으면, 해당 설정을 사용하는 프로젝트 어느 곳에서나 `일관성`있는 날짜, 시간 문자열 값을 LocalDateTime 타입 변수에 즉시 바인딩할 수 있습니다. 확실히 문자열로 받고, 이를 변환하는 기존 방식보다 훨씬 효율적이고 관리하기 쉬워졌습니다.


## 마무리

같은 고민을 하는 개발자는 반드시 1명 이상은 있는 것 같습니다. 검색하면 해결 방법이 쉽게 나옴에도 불구하고 단순히 String으로 데이터를 전달 받고 처리했던 저 자신을 반성하게 되는 계기였습니다.
