import org.apache.ibatis.annotations.Param;
import java.util.List;

public interface UserMapper {
    int getTotalNumberOfProducts();

    List<Integer> getCollectRecords(@Param("userId") String userId);

    List<Integer> getPurchaseRecords(@Param("userId") String userId);

    List<String> getAllUserIds();
}
